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
        return (first_line.strip().split(','))[0]

start_time = get_start_time(file)
folder_name = start_time.replace(':', '-')
os.makedirs('data\\' + folder_name)

shutil.copy(file, os.path.join('data', folder_name, 'data.txt'))

print("Gathering data...")

x1_data = np.array([])
y1_data = np.array([])
z1_data = np.array([])
x2_data = np.array([])
y2_data = np.array([])
z2_data = np.array([])
x3_data = np.array([])
y3_data = np.array([])
z3_data = np.array([])
x4_data = np.array([])
y4_data = np.array([])
z4_data = np.array([])
x5_data = np.array([])
y5_data = np.array([])
z5_data = np.array([])
x6_data = np.array([])
y6_data = np.array([])
z6_data = np.array([])
x7_data = np.array([])
y7_data = np.array([])
z7_data = np.array([])

marker_color = np.array([])
time_data = []

with open(os.path.join('data', folder_name, 'data.txt'), 'r') as data_file:
    for line in data_file:
        time_utc, new_x1, new_y1, new_z1, new_x2, new_y2, new_z2, new_x3, new_y3, new_z3, new_x4, new_y4, new_z4, new_x5, new_y5, new_z5, new_x6, new_y6, new_z6, new_x7, new_y7, new_z7 = line.strip().split(',')
        new_z1 = min(new_z1, 200.0)
        new_z2 = min(new_z2, 200.0)
        new_z3 = min(new_z3, 200.0)
        new_z4 = min(new_z4, 200.0)
        new_z5 = min(new_z5, 200.0)
        new_z6 = min(new_z6, 200.0)
        new_z7 = min(new_z7, 200.0)
        x1_data = np.append(x1_data, float(new_x1))
        y1_data = np.append(y1_data, float(new_y1))
        z1_data = np.append(z1_data, float(new_z1))
        x2_data = np.append(x2_data, float(new_x2))
        y2_data = np.append(y2_data, float(new_y2))
        z2_data = np.append(z2_data, float(new_z2))
        x3_data = np.append(x3_data,float(new_x3))
        y3_data = np.append(y3_data,float(new_y3))
        z3_data = np.append(z3_data, float(new_z3))
        x4_data = np.append(x4_data,float(new_x3))
        y4_data = np.append(y4_data,float(new_y4))
        z4_data = np.append(z4_data, float(new_z4))
        x5_data = np.append(x5_data,float(new_x5))
        y5_data = np.append(y5_data,float(new_y5))
        z5_data = np.append(z5_data, float(new_z5))
        x6_data = np.append(x6_data,float(new_x6))
        y6_data = np.append(y6_data,float(new_y6))
        z6_data = np.append(z6_data, float(new_z6))
        x7_data = np.append(x7_data, float(new_x7))
        y7_data = np.append(y7_data, float(new_y7))
        z7_data = np.append(z7_data, float(new_z7))

        marker_color_1 = np.append(marker_color,-float(new_z1))
        marker_color_2 = np.append(marker_color,-float(new_z2))
        marker_color_3 = np.append(marker_color,-float(new_z3))
        marker_color_4 = np.append(marker_color,-float(new_z4))
        marker_color_5 = np.append(marker_color,-float(new_z5))
        marker_color_6 = np.append(marker_color,-float(new_z6))
        marker_color_7 = np.append(marker_color,-float(new_z7))
        time_data.append(time_utc)

print("Smoothing things out...")

smoothed_z1_data = moving_average(z1_data, 2)
smoothed_z2_data = moving_average(z3_data, 2)
smoothed_z3_data = moving_average(z3_data, 2)
smoothed_z4_data = moving_average(z4_data, 2)
smoothed_z5_data = moving_average(z5_data, 2)
smoothed_z6_data = moving_average(z6_data, 2)
smoothed_z7_data = moving_average(z7_data, 2)

print("Plotting...")

trace3d = go.Scatter3d(x=x1_data, y=y1_data, z=z1_data, mode='lines+markers', name='Array 1', marker=dict(size=5, color=marker_color_1, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
trace3d_1 = go.Scatter3d(x=x2_data, y=y2_data, z=z2_data, mode='lines+markers', name='Array 2', marker=dict(size=5, color=marker_color_2, colorscale='Viridis', opacity=0.8), line=dict(color='darkred', width=2))
trace3d_2 = go.Scatter3d(x=x3_data, y=y3_data, z=z3_data, mode='lines+markers', name='Array 3', marker=dict(size=5, color=marker_color_3, colorscale='Viridis', opacity=0.8), line=dict(color='darkgreen', width=2))
trace3d_3 = go.Scatter3d(x=x4_data,y=y4_data,z=z4_data,mode='lines+markers',name='Array 4',marker=dict(size=5,color=marker_color_4,colorscale='Viridis',opacity=0.8),line=dict(color='darkorange',width=2))
trace3d_4 = go.Scatter3d(x=x5_data,y=y5_data,z=z5_data,mode='lines+markers',name='Array 5',marker=dict(size=5,color=marker_color_5,colorscale='Viridis',opacity=0.8),line=dict(color='violet',width=2))
trace3d_5 = go.Scatter3d(x=x6_data,y=y6_data,z=z6_data,mode='lines+markers',name='Array 6',marker=dict(size=5,color=marker_color_6,colorscale='Viridis',opacity=0.8),line=dict(color='darkturquoise',width=2))
trace3d_6 = go.Scatter3d(x=x7_data,y=y7_data,z=z7_data,mode='lines+markers',name='Array 7',marker=dict(size=5,color=marker_color_7,colorscale='Viridis',opacity=0.8),line=dict(color='darkslategray',width=2))

data3d = [trace3d, trace3d_1, trace3d_2, trace3d_3 , trace3d_4 , trace3d_5 , trace3d_6]
layout3d = go.Layout(scene=dict(xaxis_title='Distance X (m)', yaxis_title='Distance Y (m)', zaxis=dict(title='Distance Z (cm)', autorange='reversed')), margin=dict(l=0, r=0, b=0, t=0))
fig3d = go.Figure(data=data3d, layout=layout3d)
plotly.offline.plot(fig3d, filename=os.path.join('data', folder_name, 'map.html'), auto_open=False)

trace2d = go.Scatter(x=time_data, y=z1_data, mode='lines+markers', name='Array 1', marker=dict(size=5, color=marker_color_1, colorscale='Viridis', opacity=0.8), line=dict(color='darkblue', width=2))
trace2d_1 = go.Scatter(x=time_data, y=z2_data, mode='lines+markers', name='Array 2', marker=dict(size=5, color=marker_color_2, colorscale='Viridis', opacity=0.8), line=dict(color='darkred', width=2))
trace2d_2 = go.Scatter(x=time_data, y=z3_data, mode='lines+markers', name='Array 3', marker=dict(size=5, color=marker_color_3, colorscale='Viridis', opacity=0.8), line=dict(color='darkgreen', width=2))
trace2d_3 = go.Scatter(x=time_data,y=z4_data,mode='lines+markers',name='Array 4',marker=dict(size=5,color=marker_color_4,colorscale='Viridis',opacity=0.8),line=dict(color='darkorange',width=2))
trace2d_4 = go.Scatter(x=time_data,y=z5_data,mode='lines+markers',name='Array 5',marker=dict(size=5,color=marker_color_5,colorscale='Viridis',opacity=0.8),line=dict(color='violet',width=2))
trace2d_5 = go.Scatter(x=time_data,y=z6_data,mode='lines+markers',name='Array 6',marker=dict(size=5,color=marker_color_6,colorscale='Viridis',opacity=0.8),line=dict(color='darkturquoise',width=2))
trace2d_6 = go.Scatter(x=time_data,y=z7_data,mode='lines+markers',name='Array 7',marker=dict(size=5,color=marker_color_7,colorscale='Viridis',opacity=0.8),line=dict(color='darkslategray',width=2))

data2d = [trace2d, trace2d_1, trace2d_2, trace2d_3 , trace2d_4 , trace2d_5 , trace2d_6]
layout2d = go.Layout(xaxis_title='Time (s)', yaxis=dict(title='Distance (cm)', autorange='reversed'), margin=dict(l=0, r=0, b=0, t=0))
fig2d = go.Figure(data=data2d, layout=layout2d)
plotly.offline.plot(fig2d, filename=os.path.join('data', folder_name, 'graph.html'), auto_open=False)

print("Done")
