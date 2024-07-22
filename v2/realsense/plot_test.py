import pyrealsense2 as rs
import numpy as np
import plotly.graph_objects as go
import time

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)

profile = pipeline.start(config)

align_to = rs.stream.color
align = rs.align(align_to)

print("Warming up the camera...")
warm_up_frames = 10
for i in range(warm_up_frames):
    pipeline.wait_for_frames()
    time.sleep(0.1)
print("Warm-up complete.")

try:
    frames = pipeline.wait_for_frames()
    
    aligned_frames = align.process(frames)
    
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    
    if not aligned_depth_frame or not color_frame:
        raise RuntimeError("Could not acquire valid frames")
    
    pc = rs.pointcloud()
    points = pc.calculate(aligned_depth_frame)
    
    vtx = np.asanyarray(points.get_vertices())
    
    vtx = np.array([(v[0], v[1], v[2]) for v in vtx])
    
    vtx = vtx[np.any(vtx != 0, axis=1)]
    
    downsample_factor = 1
    downsampled_vtx = vtx[::downsample_factor]
    
    print(f"Number of points in original cloud: {len(vtx)}")
    print(f"Number of points after downsampling: {len(downsampled_vtx)}")
    
    fig = go.Figure(data=[go.Scatter3d(
        x=downsampled_vtx[:, 0],
        y=downsampled_vtx[:, 1],
        z=downsampled_vtx[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=downsampled_vtx[:, 2],
            colorscale='Viridis',
            opacity=1
        )
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
        title='RealSense High-Resolution Downsampled Point Cloud'
    )
    
    fig.write_html("realsense_highres_downsampled_pointcloud.html")
    print("High-resolution downsampled point cloud visualization saved as 'realsense_highres_downsampled_pointcloud.html'")

finally:
    pipeline.stop()