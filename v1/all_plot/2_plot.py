import serial, utm, plotly.graph_objs as go, plotly, os, time, numpy as np, logging

ar_ser, em_ser = "COM3", "COM4"
# COM 9 ''' ulr_ard || COM7 ''' /dev/gps_tail

print("Please wait...")
date = start_time = None

def parse_nmea_data(data):
    global date, start_time, last_direction
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNZDA":
        date = "00-00-0000" if data[4] == "" else f"{data[4]}-{data[3]}-{data[2]}"
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}" if date != "00-00-0000" else "00-00-0000_00:00:00"
        start_time = time_utc
        if start_time is None:
            try:
                os.makedirs(f"data/{time_utc.replace(':', '-')}")
            except FileExistsError:
                a = 0
        return time_utc

    if data_type == "GNGGA" and date is not None:
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}" if date != "00-00-0000" else "00-00-0000_00:00:00"
        lat = lon = None

        print(f"time:{time_utc}, 0, 0")
        return ("00:00:00", 0, 0) if lat is None or lon is None else (time_utc, lat, lon)
        # return time_utc, lat, lon

    if data_type == "GNRMC" and date is not None:
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}"
        if data[8] != '':
            last_direction = float(data[8])

def moving_average(data, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(data, window, 'valid')

def calculate_new_points(x, y, direction, distance):
    angle = np.deg2rad(direction + 90)
    dx, dy = distance/2 * np.sin(angle), distance/2 * np.cos(angle)
    new_x1, new_y1, new_x2, new_y2 = x + dx, y + dy, x - dx, y - dy
    
    return new_x1, new_y1, new_x2, new_y2

emlid = serial.Serial(em_ser, 11520, timeout=.1)
arduino = serial.Serial(ar_ser, 9600, timeout=.1)

time.sleep(1)
emlid.flushInput()
arduino.flushInput()

origin_set, ded = False, False
origin_x, origin_y, last_direction = 0, 0, 0
x, y = 1, 1

time.sleep(0.1)

while start_time is None:
    if emlid.in_waiting > 0:
        data = emlid.readline().decode('ascii', errors='replace')
        parse_nmea_data(data)

folder_name = start_time.replace(':', '-')
folder_path = os.path.join('data', folder_name)

while not os.path.exists(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
    except FileExistsError:
        print("Data already exists")

try:
    with open(os.path.join(folder_path, 'data.txt'), 'w') as data_file:
    
        while True:
            if emlid.in_waiting > 0:
                data = emlid.readline().decode('ascii', errors='replace')
                parsed_data = parse_nmea_data(data)
                if parsed_data and isinstance(parsed_data, tuple):
                    if arduino.in_waiting > 0:
                        distances = (arduino.readline()[:-1].decode('ascii', errors='replace')).strip().split(', ')
                        d1, d2 = float(distances[0]), float(distances[1])
                        ded = True

                    if ded and last_direction is not None:
                        time_utc, lat, lon = parsed_data
                        print(f"[Rover] Time: {time_utc}, Lat: {lat}, Lon: {lon}, Dist: {d1}, {d2} cm")

                        x, y, _, _ = utm.from_latlon(lat, lon)

                    if not origin_set:
                        origin_x, origin_y = x, y
                        origin_set = True

                    rel_x, rel_y = x - origin_x, y - origin_y

                    # new_x1, new_y1, new_x2, new_y2, new_x3, new_y3, new_x5, new_y5, new_x6, new_y6, new_x7, new_y7 = calculate_new_points(rel_x, rel_y, last_direction, 1.7)

                    data_file.write(f"{time_utc}, {rel_x}, {rel_y}, {last_direction}, {d1}, {d2}\n")
                    data_file.flush()

except KeyboardInterrupt:
    print("Gathering data...")

    x1_data, y1_data, z1_data, x2_data, y2_data, z2_data = np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])

    marker_color, time_data = np.array([]), []

    with open(os.path.join('data', folder_name, 'data.txt'), 'r') as data_file:
        for line in data_file:
            time_utc, new_x4, new_y4, last_direction, new_z1, new_z2 = line.strip().split(',')
            new_z1, new_z2 = min(float(new_z1), 200.0), min(float(new_z2), 200.0)

            new_x1, new_y1, new_x2, new_y2 = calculate_new_points(float(new_x4), float(new_y4), float(last_direction), 1.7)
            x1_data, y1_data, z1_data, x2_data, y2_data, z2_data = np.append(x1_data, float(new_x1)), np.append(y1_data, float(new_y1)), np.append(z1_data, float(new_z1)), np.append(x2_data, float(new_x2)), np.append(y2_data, float(new_y2)), np.append(z2_data, float(new_z2))

            marker_color_1, marker_color_2 = np.append(marker_color, -float(new_z1)), np.append(marker_color, -float(new_z2))
            time_data.append(time_utc)

    print("Smoothing things out...")

    window = 2
    smoothed_z1_data, smoothed_z2_data = moving_average(z1_data, window), moving_average(z2_data, window)

    print("Plotting...")

    trace3d = go.Scatter3d(x=x1_data, y=y1_data, z=z1_data, mode='lines+markers', name='Array 1', marker=dict(size=5, color=marker_color_1, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
    trace3d_1 = go.Scatter3d(x=x2_data, y=y2_data, z=z2_data, mode='lines+markers', name='Array 2', marker=dict(size=5, color=marker_color_2, colorscale='Viridis', opacity=0.8), line=dict(color='darkred', width=2))

    data3d = [trace3d, trace3d_1]
    layout3d = go.Layout(scene=dict(xaxis_title='Distance X (m)', yaxis_title='Distance Y (m)', zaxis=dict(title='Distance Z (cm)', autorange='reversed')), margin=dict(l=0, r=0, b=0, t=0))
    fig3d = go.Figure(data=data3d, layout=layout3d)
    plotly.offline.plot(fig3d, filename=os.path.join('data', folder_name, 'map.html'), auto_open=False)

    trace2d = go.Scatter(x=time_data, y=z1_data, mode='lines+markers', name='Array 1', marker=dict(size=5, color=marker_color_1, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
    trace2d_1 = go.Scatter(x=time_data, y=z2_data, mode='lines+markers', name='Array 2', marker=dict(size=5, color=marker_color_2, colorscale='Viridis', opacity=0.8), line=dict(color='darkred', width=2))

    data2d = [trace2d, trace2d_1]
    layout2d = go.Layout(xaxis_title='Time (s)', yaxis=dict(title='Distance (cm)', autorange='reversed'), margin=dict(l=0, r=0, b=0, t=0))
    fig2d = go.Figure(data=data2d, layout=layout2d)
    plotly.offline.plot(fig2d, filename=os.path.join('data', folder_name, 'graph.html'), auto_open=False)

print("Done")
