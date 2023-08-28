import numpy as np
import os
import plotly.graph_objs as go
import plotly
import shutil
from datetime import datetime, timedelta

file1 = input("Data no boom path 1: ")
file2 = input("Data boom path 2: ")

def get_start_time(file):
    with open(file, 'r') as data_file:
        first_line = data_file.readline()
        return (first_line.strip().split(','))[0]

start_time1 = datetime.strptime(get_start_time(file1), "%Y-%m-%d_%H:%M:%S.%f")
start_time2 = datetime.strptime(get_start_time(file2), "%Y-%m-%d_%H:%M:%S.%f")

start_time = min(start_time1, start_time2)

z_data1, z_data2 = np.array([]), np.array([])
time_data1, time_data2 = [], []

with open(file1, 'r') as data_file:
    for line in data_file:
        time_utc, _, _, _, new_z1, new_z2, new_z3, new_z4, new_z5, new_z6, new_z7 = line.strip().split(',')
        avg_z = np.mean([float(new_z1), float(new_z2), float(new_z3), float(new_z4), float(new_z5), float(new_z6), float(new_z7)])
        z_data1 = np.append(z_data1, avg_z)
        time_data1.append((datetime.strptime(time_utc, "%Y-%m-%d_%H:%M:%S.%f") - start_time1).total_seconds())

with open(file2, 'r') as data_file:
    for line in data_file:
        time_utc, _, _, _, new_z1, new_z2, new_z3, new_z4, new_z5, new_z6, new_z7 = line.strip().split(',')
        avg_z = np.mean([float(new_z1), float(new_z2), float(new_z3), float(new_z4), float(new_z5), float(new_z6), float(new_z7)])
        z_data2 = np.append(z_data2, avg_z)
        time_data2.append((datetime.strptime(time_utc, "%Y-%m-%d_%H:%M:%S.%f") - start_time2).total_seconds())

print("Plotting...")

trace2d_1 = go.Scatter(x=time_data1, y=z_data1, mode='lines+markers', name='No Boom', marker=dict(size=5, color='blue', opacity=0.8), line=dict(color='darkblue', width=2))
trace2d_2 = go.Scatter(x=time_data2, y=z_data2, mode='lines+markers', name='Boom Run', marker=dict(size=5, color='red', opacity=0.8), line=dict(color='darkred', width=2))

data2d = [trace2d_1, trace2d_2]
layout2d = go.Layout(xaxis_title='Time Since Start (s)', yaxis=dict(title='Average Distance (cm)', autorange='reversed'), margin=dict(l=0, r=0, b=0, t=0))
fig2d = go.Figure(data=data2d, layout=layout2d)
plotly.offline.plot(fig2d, filename=os.path.join('data', 'noboomrun2boomrun1.html'), auto_open=False)

print("Done")