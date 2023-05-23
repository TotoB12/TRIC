import serial
import utm
import plotly.graph_objs as go
import plotly
import os
import datetime
import time
import keyboard
import numpy as np

array_spacing = float(input("Array spacing (m): "))
print("Please wait...")

date = None
start_time = None
last_direction = None

def parse_nmea_data(data):
    global date, start_time, last_direction
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

    if data_type == "GNRMC" and date is not None:
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}"
        if data[8] != '':
            last_direction = float(data[8])

def moving_average(data, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(data, window, 'valid')

def calculate_new_points(x, y, d, direction, distance):
    angle = np.deg2rad(direction + 90)
    dx = distance * np.sin(angle)
    dy = distance * np.cos(angle)
    new_x1 = x + dx
    new_y1 = y + dy
    new_x2 = x - dx
    new_y2 = y - dy
    new_x3 = x + 2 * dx
    new_y3 = y + 2 * dy
    new_x4 = x - 2 * dx
    new_y4 = y - 2 * dy
    new_x5 = x + 3 * dx
    new_y5 = y + 3 * dy
    new_x6 = x - 3 * dx
    new_y6 = y - 3 * dy
    new_x7 = x + 4 * dx
    new_y7 = y + 4 * dy
    
    return new_x1, new_y1, new_x2, new_y2,new_x3,new_y3,new_x4,new_y4,new_x5,new_y5,new_x6,new_y6,new_x7,new_y7


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
    folder_path = os.path.join('data', folder_name)
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, 'data.txt'), 'w') as data_file:

        while True:
            if emlid.in_waiting > 0:
                data = emlid.readline().decode('ascii', errors='replace')
                parsed_data = parse_nmea_data(data)
                if parsed_data and isinstance(parsed_data, tuple):
                    if arduino.in_waiting > 0:
                        distance = arduino.readline()[:-1].decode('ascii', errors='replace')
                        d = float(distance)
                        ded = True

                    if ded and last_direction is not None:
                        time_utc, lat, lon = parsed_data
                        print(f"[Rover] Time: {time_utc}, Lat: {lat}, Lon: {lon}, Dist: {d} cm")

                        x, y, _, _ = utm.from_latlon(lat, lon)

                    if not origin_set:
                        origin_x, origin_y = x, y
                        origin_set = True

                    rel_x = x - origin_x
                    rel_y = y - origin_y

                    new_x1, new_y1, new_x2, new_y2,new_x3,new_y3,new_x4,new_y4,new_x5,new_y5,new_x6,new_y6,new_x7,new_y7= calculate_new_points(rel_x,
                                                                                                                                                rel_y,
                                                                                                                                                d,
                                                                                                                                                last_direction,
                                                                                                                                                array_spacing)

                    data_file.write(f"{time_utc}, {rel_x}, {rel_y}, {d}, {new_x1}, {new_y1}, {new_x2}, {new_y2}, {new_x3}, {new_y3}, {new_x4}, {new_y4}, {new_x5}, {new_y5}, {new_x6}, {new_y6}, {new_x7}, {new_y7}\n")
                    data_file.flush()

except KeyboardInterrupt:
    print("Plotting...")

    x_data = np.array([])
    y_data = np.array([])
    z_data = np.array([])
    x1_data = np.array([])
    y1_data = np.array([])
    x2_data = np.array([])
    y2_data = np.array([])
    x3_data = np.array([])
    y3_data = np.array([])
    x4_data = np.array([])
    y4_data = np.array([])
    x5_data = np.array([])
    y5_data = np.array([])
    x6_data = np.array([])
    y6_data = np.array([])
    x7_data = np.array([])
    y7_data = np.array([])

    marker_color = np.array([])
    time_data = []
    
    with open(os.path.join('data', folder_name, 'data.txt'), 'r') as data_file:
            for line in data_file:
                time_utc, rel_x, rel_y, d, new_x1, new_y1, new_x2, new_y2,new_x3,new_y3,new_x4,new_y4,new_x5,new_y5,new_x6,new_y6,new_x7,new_y7= line.strip().split(',')
                x_data = np.append(x_data, float(rel_x))
                y_data = np.append(y_data, float(rel_y))
                z_data = np.append(z_data, float(d))
                x1_data = np.append(x1_data, float(new_x1))
                y1_data = np.append(y1_data, float(new_y1))
                x2_data = np.append(x2_data, float(new_x2))
                y2_data = np.append(y2_data, float(new_y2))
                x3_data = np.append(x3_data,float(new_x3))
                y3_data=np.append(y3_data,float(new_y3))
                x4_data=np.append(x4_data,float(new_x4))
                y4_data=np.append(y4_data,float(new_y4))
                x5_data=np.append(x5_data,float(new_x5))
                y5_data=np.append(y5_data,float(new_y5))
                x6_data=np.append(x6_data,float(new_x6))
                y6_data=np.append(y6_data,float(new_y6))
                x7_data=np.append(x7_data,float(new_x7))
                y7_data=np.append(y7_data,float(new_y7))

                marker_color = np.append(marker_color,-float(d))
                time_data.append(time_utc)

                smoothed_z_data = moving_average(z_data, 2)

                trace3d = go.Scatter3d(x=x_data, y=y_data, z=smoothed_z_data, mode='lines+markers', name='Array 4', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
                trace3d_1 = go.Scatter3d(x=x1_data, y=y1_data, z=smoothed_z_data, mode='lines+markers', name='Array 1', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkred', width=2))
                trace3d_2 = go.Scatter3d(x=x2_data, y=y2_data, z=smoothed_z_data, mode='lines+markers', name='Array 2', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkgreen', width=2))
                trace3d_3 = go.Scatter3d(x=x3_data,y=y3_data,z=smoothed_z_data,mode='lines+markers',name='Array 3',marker=dict(size=5,color=marker_color,colorscale='Viridis',opacity=0.8),line=dict(color='darkorange',width=2))
                trace3d_4 = go.Scatter3d(x=x4_data,y=y4_data,z=smoothed_z_data,mode='lines+markers',name='Array 5',marker=dict(size=5,color=marker_color,colorscale='Viridis',opacity=0.8),line=dict(color='violet',width=2))
                trace3d_5 = go.Scatter3d(x=x5_data,y=y5_data,z=smoothed_z_data,mode='lines+markers',name='Array 6',marker=dict(size=5,color=marker_color,colorscale='Viridis',opacity=0.8),line=dict(color='darkturquoise',width=2))
                trace3d_6 = go.Scatter3d(x=x6_data,y=y6_data,z=smoothed_z_data,mode='lines+markers',name='Array 7',marker=dict(size=5,color=marker_color,colorscale='Viridis',opacity=0.8),line=dict(color='darkslategray',width=2))

                data3d = [trace3d, trace3d_1, trace3d_2, trace3d_3 , trace3d_4 , trace3d_5 , trace3d_6]
                layout3d = go.Layout(scene=dict(xaxis_title='Distance X (m)', yaxis_title='Distance Y (m)', zaxis=dict(title='Distance Z (cm)', autorange='reversed')), margin=dict(l=0, r=0, b=0, t=0))
                fig3d = go.Figure(data=data3d, layout=layout3d)
                plotly.offline.plot(fig3d, filename=os.path.join('data', folder_name, 'map.html'), auto_open=False)

                trace2d = go.Scatter(x=time_data, y=smoothed_z_data, mode='lines+markers', name='Array 4', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
                trace2d_1 = go.Scatter(x=time_data, y=smoothed_z_data, mode='lines+markers', name='Array 1', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkred', width=2))
                trace2d_2 = go.Scatter(x=time_data, y=smoothed_z_data, mode='lines+markers', name='Array 2', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkgreen', width=2))
                trace2d_3 = go.Scatter(x=time_data,y=smoothed_z_data,mode='lines+markers',name='Array 3',marker=dict(size=5,color=marker_color,colorscale='Viridis',opacity=0.8),line=dict(color='darkorange',width=2))
                trace2d_4 = go.Scatter(x=time_data,y=smoothed_z_data,mode='lines+markers',name='Array 5',marker=dict(size=5,color=marker_color,colorscale='Viridis',opacity=0.8),line=dict(color='violet',width=2))
                trace2d_5 = go.Scatter(x=time_data,y=smoothed_z_data,mode='lines+markers',name='Array 6',marker=dict(size=5,color=marker_color,colorscale='Viridis',opacity=0.8),line=dict(color='darkturquoise',width=2))
                trace2d_6 = go.Scatter(x=time_data,y=smoothed_z_data,mode='lines+markers',name='Array 7',marker=dict(size=5,color=marker_color,colorscale='Viridis',opacity=0.8),line=dict(color='darkslategray',width=2))

                data2d = [trace2d, trace2d_1, trace2d_2, trace2d_3 , trace2d_4 , trace2d_5 , trace2d_6]
                layout2d = go.Layout(xaxis_title='Time (s)', yaxis=dict(title='Distance (cm)', autorange='reversed'), margin=dict(l=0, r=0, b=0, t=0))
                fig2d = go.Figure(data=data2d, layout=layout2d)
                plotly.offline.plot(fig2d, filename=os.path.join('data', folder_name, 'graph.html'), auto_open=False)

print("Done")
