import os
import numpy as np
import plotly.graph_objs as go
from scipy.interpolate import griddata
from scipy.spatial import Delaunay
from plyfile import PlyData, PlyElement

MAX_ELEVATION = 0.5
MIN_ELEVATION = -10
DOWNSAMPLE_FACTOR = 10  # 1 for no downsampling
Z_SCALE_FACTOR = 0.4  # 1 for 1:1

def load_data(data_path):
    txt_file = os.path.join(data_path, 'processed_data.txt')
    folder = os.path.join(data_path, 'processed_data')
    
    if os.path.isfile(txt_file):
        processed_data = np.loadtxt(txt_file, delimiter=',')
    elif os.path.isdir(folder):
        all_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.txt')]
        processed_data = []
        for file in all_files:
            data = np.loadtxt(file, delimiter=',')
            processed_data.append(data)
        processed_data = np.vstack(processed_data)
    else:
        raise ValueError("Provided path does not contain 'processed_data.txt' or 'processed_data' folder.")
    
    return processed_data

def save_as_ply(file_path, x, y, z):
    vertices = np.array([x, y, z], dtype=np.float32).T
    vertices = [tuple(vertex) for vertex in vertices]
    vertex_elements = np.array(vertices, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])

    points2D = np.vstack([x, y]).T
    tri = Delaunay(points2D)
    faces = tri.simplices
    face_elements = np.array([(face,) for face in faces], dtype=[('vertex_indices', 'i4', (3,))])

    ply_element_vertex = PlyElement.describe(vertex_elements, 'vertex')
    ply_element_face = PlyElement.describe(face_elements, 'face')
    ply_data = PlyData([ply_element_vertex, ply_element_face], text=True)
    ply_data.write(file_path)

def plot_data(data_folder, max_elevation, min_elevation, downsample_factor):
    print("Plotting data...")
    try:
        processed_data = load_data(data_folder)

        if processed_data.size == 0 or processed_data.ndim == 1:
            print("Insufficient data for plotting.")
            return

        processed_data = processed_data[(processed_data[:, 2] >= min_elevation) & (processed_data[:, 2] <= max_elevation)]

        if downsample_factor > 1:
            processed_data = processed_data[::downsample_factor]

        x, y, z = processed_data[:, 0], processed_data[:, 1], processed_data[:, 2]

        x_rel = x - np.min(x)
        y_rel = y - np.min(y)

        x_range = np.ptp(x_rel)
        y_range = np.ptp(y_rel)
        z_range = np.ptp(z)
        
        max_range = max(x_range, y_range)
        z_scale = max_range / z_range * Z_SCALE_FACTOR

        fig_3d = go.Figure()

        fig_3d.add_trace(go.Scatter3d(
            x=x_rel,
            y=y_rel,
            z=z,
            mode='markers',
            marker=dict(
                size=2,
                color=z,
                colorscale='Balance',
                opacity=1,
                colorbar=dict(title='Elevation (m)')
            ),
            name='All Points'
        ))

        fig_3d.update_layout(
            scene=dict(
                aspectmode='manual',
                aspectratio=dict(x=x_range, y=y_range, z=z_range*z_scale),
                xaxis=dict(range=[0, x_range]),
                yaxis=dict(range=[0, y_range]),
                zaxis=dict(range=[np.min(z), np.max(z)]),
                xaxis_title='Relative Easting (m)',
                yaxis_title='Relative Northing (m)',
                zaxis_title='Elevation (mm)'
            ),
            title='3D Scatter Plot',
            template='plotly_dark'
        )
        fig_3d.write_html(os.path.join(data_folder, '3d_scatter_plot.html'))

        fig_2d = go.Figure(data=[go.Scatter(
            x=x_rel,
            y=y_rel,
            mode='markers',
            marker=dict(
                size=2,
                color=z,
                colorscale='Balance',
                opacity=1,
                colorbar=dict(title='Elevation (mm)')
            )
        )])
        fig_2d.update_layout(
            xaxis_title='Relative Easting (m)',
            yaxis_title='Relative Northing (m)',
            title='2D Scatter Plot',
            template='plotly_dark'
        )
        fig_2d.write_html(os.path.join(data_folder, '2d_scatter_plot.html'))

        save_as_ply(os.path.join(data_folder, 'point_cloud.ply'), x_rel, y_rel, z)

        print(f"Plots and 3D file saved in {data_folder}")
    except Exception as e:
        print(f"An error occurred while plotting: {str(e)}")

if __name__ == "__main__":
    path = input("Enter the path to the data folder or file: ")
    if os.path.exists(path):
        try:
            plot_data(path, MAX_ELEVATION, MIN_ELEVATION, DOWNSAMPLE_FACTOR)
        except ValueError:
            print("Invalid input for maximum elevation or downsampling factor.")
    else:
        print("Invalid folder or file path.")
