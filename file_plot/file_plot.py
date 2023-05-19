import numpy as np
import os
import datetime
import utm
import plotly.graph_objs as go
import plotly
import shutil

file = input("Data file path: ")

def moving_average(data, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(data, window, 'valid')

def get_start_time(file):
    with open(file, 'r') as data_file:
        first_line = data_file.readline()
        time_utc, _, _, _ = first_line.strip().split(',')
        return time_utc

start_time = get_start_time(file)
folder_name = start_time.replace(':', '-')
os.makedirs('data\\' + folder_name)

shutil.copy(file, os.path.join('data', folder_name, 'data.txt'))

print("Plotting...")

x_data = np.array([])
y_data = np.array([])
z_data = np.array([])
marker_color = np.array([])
time_data = []

with open(os.path.join(file), 'r') as data_file:
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

trace2d = go.Scatter(x=time_data, y=z_data, mode='lines+markers', marker=dict(size=5, color=marker_color, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
data2d = [trace2d]
layout2d = go.Layout(xaxis_title='Time (s)', yaxis=dict(title='Distance (cm)', autorange='reversed'), margin=dict(l=0, r=0, b=0, t=0))
fig2d = go.Figure(data=data2d, layout=layout2d)
plotly.offline.plot(fig2d, filename=os.path.join('data', folder_name, 'graph.html'), auto_open=False)

print("Done")
