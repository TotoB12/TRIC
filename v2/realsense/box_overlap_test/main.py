import numpy as np
import plotly.graph_objs as go
from pyproj import Transformer

MAX_HEIGHT = 0.4

def read_cloud_file(filename):
    with open(filename, 'r') as f:
        return np.array([list(map(float, line.strip().split(','))) for line in f])

def read_gps_file(filename):
    with open(filename, 'r') as f:
        return list(map(float, f.read().strip().split(',')))

def rotate_points(points, angle_deg):
    angle_rad = np.radians(angle_deg)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1]
    ])
    return np.dot(points, rotation_matrix.T)

def main():
    cloud1 = read_cloud_file('cloud1.txt')
    cloud2 = read_cloud_file('cloud2.txt')
    cloud1 = cloud1[cloud1[:, 2] <= MAX_HEIGHT]
    cloud2 = cloud2[cloud2[:, 2] <= MAX_HEIGHT]

    gps1 = read_gps_file('gps1.txt')
    gps2 = read_gps_file('gps2.txt')

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32610", always_xy=True)

    x1, y1 = transformer.transform(gps1[1], gps1[0])
    x2, y2 = transformer.transform(gps2[1], gps2[0])

    cloud1 = rotate_points(cloud1, gps1[2])
    cloud2 = rotate_points(cloud2, gps2[2])

    cloud1 -= cloud1.mean(axis=0)
    cloud2 -= cloud2.mean(axis=0)

    translation = np.array([x2 - x1, y2 - y1, 0])
    cloud2 += translation

    trace1 = go.Scatter3d(
        x=cloud1[:, 0], y=cloud1[:, 1], z=cloud1[:, 2],
        mode='markers',
        marker=dict(size=5, color='red'),
        name='Cloud 1'
    )

    trace2 = go.Scatter3d(
        x=cloud2[:, 0], y=cloud2[:, 1], z=cloud2[:, 2],
        mode='markers',
        marker=dict(size=5, color='blue'),
        name='Cloud 2',
    )

    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='X (m)'),
            yaxis=dict(title='Y (m)'),
            zaxis=dict(title='Z (m)'),
            aspectmode='data'
        ),
        title='Combined 3D Box Without Using GPS Data',
        template='plotly_dark'
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    
    # fig.show()
    
    fig.write_html("overlap_box_nogps.html")

if __name__ == "__main__":
    main()