import numpy as np, os, plotly.graph_objs as go, plotly, shutil, utm

file = input("Data file path: ")
origin_set = False

def moving_average(data, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(data, window, 'valid')

def calculate_new_points(x, y, direction, distance):
    angle = np.deg2rad(float(direction) + 90)
    dx, dy = distance * np.sin(angle), distance * np.cos(angle)
    new_x1, new_y1, new_x2, new_y2, new_x3, new_y3, new_x4, new_y4, new_x5, new_y5, new_x6, new_y6 = x + dx, y + dy, x - dx, y - dy, x + 2 * dx, y + 2 * dy, x - 2 * dx, y - 2 * dy, x + 3 * dx, y + 3 * dy, x - 3 * dx, y - 3 * dy
    
    return new_x1, new_y1, new_x2, new_y2, new_x3, new_y3, new_x4, new_y4, new_x5, new_y5, new_x6, new_y6

def get_start_time(file):
    with open(file, 'r') as data_file:
        first_line = data_file.readline()
        return (first_line.strip().split(','))[0]

start_time = get_start_time(file)
folder_name = start_time.replace(':', '-')
os.makedirs('data\\' + folder_name)

shutil.copy(file, os.path.join('data', folder_name, 'data.txt'))

print("Gathering data...")

x1_data, y1_data, z1_data, x2_data, y2_data, z2_data, x3_data, y3_data, z3_data, x4_data, y4_data, z4_data, x5_data, y5_data, z5_data, x6_data, y6_data, z6_data, x7_data, y7_data, z7_data = np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])

marker_color, time_data = np.array([]), []

with open(os.path.join('data', folder_name, 'data.txt'), 'r') as data_file:
    for line in data_file:
        time_utc, new_x4, new_y4, last_direction, new_z1, new_z2, new_z3, new_z4, new_z5, new_z6, new_z7 = line.strip().split(',')
        new_z1, new_z2, new_z3, new_z4, new_z5, new_z6, new_z7 = min(float(new_z1), 200.0), min(float(new_z2), 200.0), min(float(new_z3), 200.0), min(float(new_z4), 200.0), min(float(new_z5), 200.0), min(float(new_z6), 200.0), min(float(new_z7), 200.0)

        new_x4, new_y4 = float(new_x4), float(new_y4)
        x, y, _, _ = utm.from_latlon(new_x4, new_y4)
        if not origin_set:
            origin_x, origin_y = x, y
            origin_set = True
        
        rel_x, rel_y = x - origin_x, y - origin_y
        new_x4, new_y4 = rel_x, rel_y
        new_x1, new_y1, new_x2, new_y2, new_x3, new_y3, new_x5, new_y5, new_x6, new_y6, new_x7, new_y7 = calculate_new_points(new_x4, new_y4, last_direction, 1.7)
        x1_data, y1_data, z1_data, x2_data, y2_data, z2_data, x3_data, y3_data, z3_data, x4_data, y4_data, z4_data, x5_data, y5_data, z5_data, x6_data, y6_data, z6_data, x7_data, y7_data, z7_data = np.append(x1_data, float(new_x1)), np.append(y1_data, float(new_y1)), np.append(z1_data, float(new_z1)), np.append(x2_data, float(new_x2)), np.append(y2_data, float(new_y2)), np.append(z2_data, float(new_z2)), np.append(x3_data, float(new_x3)), np.append(y3_data, float(new_y3)), np.append(z3_data, float(new_z3)), np.append(x4_data, float(new_x4)), np.append(y4_data, float(new_y4)), np.append(z4_data, float(new_z4)), np.append(x5_data, float(new_x5)), np.append(y5_data, float(new_y5)), np.append(z5_data, float(new_z5)),  np.append(x6_data, float(new_x6)), np.append(y6_data, float(new_y6)), np.append(z6_data, float(new_z6)), np.append(x7_data, float(new_x7)), np.append(y7_data, float(new_y7)), np.append(z7_data, float(new_z7)) 

        marker_color_1, marker_color_2, marker_color_3, marker_color_4, marker_color_5, marker_color_6, marker_color_7 = np.append(marker_color, -float(new_z1)), np.append(marker_color, -float(new_z2)), np.append(marker_color, -float(new_z3)), np.append(marker_color, -float(new_z4)), np.append(marker_color, -float(new_z5)), np.append(marker_color, -float(new_z6)), np.append(marker_color, -float(new_z7))
        time_data.append(time_utc)

print("Smoothing things out...")

window = 2
smoothed_z1_data, smoothed_z2_data, smoothed_z3_data, smoothed_z4_data, smoothed_z5_data, smoothed_z6_data, smoothed_z7_data = moving_average(z1_data, window), moving_average(z2_data, window), moving_average(z3_data, window), moving_average(z4_data, window), moving_average(z5_data, window), moving_average(z6_data, window), moving_average(z7_data, window)

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
trace2d_3 = go.Scatter(x=time_data,y=z4_data, mode='lines+markers',name='Array 4',marker=dict(size=5,color=marker_color_4,colorscale='Viridis',opacity=0.8),line=dict(color='darkorange',width=2))
trace2d_4 = go.Scatter(x=time_data,y=z5_data, mode='lines+markers',name='Array 5',marker=dict(size=5,color=marker_color_5,colorscale='Viridis',opacity=0.8),line=dict(color='violet',width=2))
trace2d_5 = go.Scatter(x=time_data,y=z6_data, mode='lines+markers',name='Array 6',marker=dict(size=5,color=marker_color_6,colorscale='Viridis',opacity=0.8),line=dict(color='darkturquoise',width=2))
trace2d_6 = go.Scatter(x=time_data,y=z7_data, mode='lines+markers',name='Array 7',marker=dict(size=5,color=marker_color_7,colorscale='Viridis',opacity=0.8),line=dict(color='darkslategray',width=2))

data2d = [trace2d, trace2d_1, trace2d_2, trace2d_3 , trace2d_4 , trace2d_5 , trace2d_6]
layout2d = go.Layout(xaxis_title='Time (s)', yaxis=dict(title='Distance (cm)', autorange='reversed'), margin=dict(l=0, r=0, b=0, t=0))
fig2d = go.Figure(data=data2d, layout=layout2d)
plotly.offline.plot(fig2d, filename=os.path.join('data', folder_name, 'graph.html'), auto_open=False)

print("Done")
