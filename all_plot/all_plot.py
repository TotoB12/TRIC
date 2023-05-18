import serial
import utm
import plotly.graph_objs as go
import plotly
import os
import datetime
import time
import keyboard
import numpy as np

print("Please wait...")

date = None
start_time = None

def parse_nmea_data(data):
    global date, start_time
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNZDA":
        date = f"{data[4]}-{data[3]}-{data[2]}"
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}"
        if start_time is None:
            start_time = time_utc
            folder_name = start_time.replace(':', '-')
            os.makedirs('data\\' + folder_name)
        return time_utc

    if data_type == "GNGGA" and date is not None:
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}"
        try:
            lat = float(data[2][:2]) + float(data[2][2:]) / 60
            if data[3] == 'S':
                lat = -lat
            lon = float(data[4][:3]) + float(data[4][3:]) / 60
            if data[5] == 'W':
                lon = -lon
        except ValueError:
            print("bad data")
            return None

        return time_utc, lat, lon

def moving_average(data, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(data, window, 'valid')

emlid = serial.Serial('COM7', 11520, timeout=.1)
arduino = serial.Serial('COM9', 9600, timeout=.1)

time.sleep(1)
emlid.flushInput()
arduino.flushInput()

origin_set = False
origin_x, origin_y = 0, 0

ded = False

time.sleep(0.1)

while start_time is None:
    if emlid.in_waiting > 0:
        data = emlid.readline().decode('ascii', errors='replace')
        parse_nmea_data(data)

folder_name = start_time.replace(':', '-')

try:
    with open(os.path.join('data', folder_name, 'data.txt'), 'w') as data_file:
        while True:
            if emlid.in_waiting > 0:
                data = emlid.readline().decode('ascii', errors='replace')
                parsed_data = parse_nmea_data(data)
                if parsed_data:
                    if isinstance(parsed_data, tuple):
                        if arduino.in_waiting > 0:
                            distance = arduino.readline()[:-1].decode('ascii', errors='replace')
                            d = float(distance)
                            ded = True

                        if ded:
                            time_utc, lat, lon = parsed_data
                            print(f"[Rover] Time: {time_utc}, Lat: {lat}, Lon: {lon}, Dist: {d} cm")

                            x, y, _, _ = utm.from_latlon(lat, lon)

                            if not origin_set:
                                origin_x, origin_y = x, y
                                origin_set = True

                            rel_x = x - origin_x
                            rel_y = y - origin_y

                            data_file.write(f"{time_utc}, {rel_x}, {rel_y}, {d}\n")
                            data_file.flush()

except KeyboardInterrupt:
    print("Plotting...")

    x_data = np.array([])
    y_data = np.array([])
    z_data = np.array([])
    marker_color = np.array([])
    time_data = []
    with open(os.path.join('data', folder_name, 'data.txt'), 'r') as data_file:
        for line in data_file:
            time_utc, rel_x, rel_y, d = line.strip().split(',')
            x_data = np.append(x_data, float(rel_x))
            y_data = np.append(y_data, float(rel_y))
            z_data = np.append(z_data, float(d))
            marker_color = np.append(marker_color, -float(d))
            time_data.append(time_utc)

    smoothed_z_data = moving_average(z_data, 2)

    trace3d = go.Scatter3d(x=x_data, y=y_data, z=smoothed_z_data, mode='lines+markers', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
    data3d = [trace3d]
    layout3d = go.Layout(scene=dict(xaxis_title='Distance X (m)', yaxis_title='Distance Y (m)', zaxis=dict(title='Distance Z (cm)', autorange='reversed')), margin=dict(l=0, r=0, b=0, t=0))
    fig3d = go.Figure(data=data3d, layout=layout3d)
    plotly.offline.plot(fig3d, filename=os.path.join('data', folder_name, 'map.html'), auto_open=False)

    trace2d = go.Scatter(x=time_data, y=smoothed_z_data, mode='lines+markers', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
    data2d = [trace2d]
    layout2d = go.Layout(xaxis_title='Time (s)', yaxis=dict(title='Distance (cm)', autorange='reversed'), margin=dict(l=0, r=0, b=0, t=0))
    fig2d = go.Figure(data=data2d, layout=layout2d)
    plotly.offline.plot(fig2d, filename=os.path.join('data', folder_name, 'graph.html'), auto_open=False)
    
print("Done")
