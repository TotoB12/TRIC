import serial
import utm
import plotly.graph_objs as go
import plotly
import os
import datetime
import time
import keyboard
import numpy as np

def parse_nmea_data(data):
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNGGA":
        time_utc = data[1][:2] + ":" + data[1][2:4] + ":" + data[1][4:]
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

origin_set = False
origin_x, origin_y = 0, 0

x_data = np.array([])
y_data = np.array([])
z_data = np.array([])
marker_color = np.array([])

time_data = []

start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

folder_name = start_time
os.makedirs('data\\' + folder_name)

time.sleep(0.1)

with open(os.path.join('data', folder_name, 'data.txt'), 'w') as data_file:
    while True:
        if emlid.in_waiting > 0:
            data = emlid.readline().decode('ascii', errors='replace')
            parsed_data = parse_nmea_data(data)
            if parsed_data:
                if arduino.in_waiting > 0:
                    distance = arduino.readline()[:-1].decode('ascii', errors='replace')
                    d = float(distance)
                time_utc, lat, lon = parsed_data
                print(f"[Rover] Time: {time_utc}, Lat: {lat}, Lon: {lon}, Dist: {d} cm")

                x, y, _, _ = utm.from_latlon(lat, lon)

                if not origin_set:
                    origin_x, origin_y = x, y
                    origin_set = True

                rel_x = x - origin_x
                rel_y = y - origin_y

                x_data = np.append(x_data, rel_x)
                y_data = np.append(y_data, rel_y)
                z_data = np.append(z_data, d)
                marker_color = np.append(marker_color, d)

                time_data.append(time.time())

                data_file.write(f"{time_utc}, {rel_x}, {rel_y}, {d}\n")
                data_file.flush()
                
        if keyboard.is_pressed('s') or keyboard.is_pressed('c'):
            trace3d = go.Scatter3d(x=x_data, y=y_data, z=z_data, mode='lines+markers', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
            data3d = [trace3d]
            layout3d = go.Layout(scene=dict(xaxis_title='Distance X (m)', yaxis_title='Distance Y (m)', zaxis_title='Distance Z (cm)'), margin=dict(l=0, r=0, b=0, t=0))
            fig3d = go.Figure(data=data3d, layout=layout3d)
            plotly.offline.plot(fig3d, filename=os.path.join('data', folder_name, 'map.html'), auto_open=False)

            trace2d = go.Scatter(x=time_data, y=z_data, mode='lines+markers', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
            data2d = [trace2d]
            layout2d = go.Layout(xaxis_title='Time (s)', yaxis_title='Distance (cm)', margin=dict(l=0, r=0, b=0, t=0))
            fig2d = go.Figure(data=data2d, layout=layout2d)
            plotly.offline.plot(fig2d, filename=os.path.join('data', folder_name, 'graph.html'), auto_open=False)

            smoothed_z_data = moving_average(z_data, 5)

            trace2d = go.Scatter(x=time_data, y=smoothed_z_data, mode='lines+markers', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
            data2d = [trace2d]
            layout2d = go.Layout(xaxis_title='Time (s)', yaxis_title='Distance (cm)', margin=dict(l=0, r=0, b=0, t=0))
            fig2d = go.Figure(data=data2d, layout=layout2d)
            plotly.offline.plot(fig2d, filename=os.path.join('data', folder_name, 'smooth_5_graph.html'), auto_open=False)

            smoothed_z_data = moving_average(z_data, 2)

            trace2d = go.Scatter(x=time_data, y=smoothed_z_data, mode='lines+markers', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
            data2d = [trace2d]
            layout2d = go.Layout(xaxis_title='Time (s)', yaxis_title='Distance (cm)', margin=dict(l=0, r=0, b=0, t=0))
            fig2d = go.Figure(data=data2d, layout=layout2d)
            plotly.offline.plot(fig2d, filename=os.path.join('data', folder_name, 'smooth_2_graph.html'), auto_open=False)

            break