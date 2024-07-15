import pyrealsense2 as rs
import numpy as np
import rtabmap as rtab
import time
from rtabmap import rtabmap as rtabmap_process

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 63)
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)

# Start streaming
pipeline.start(config)

align_to = rs.stream.color
align = rs.align(align_to)

print("Warming up the camera...")
warm_up_frames = 10
for i in range(warm_up_frames):
    pipeline.wait_for_frames()
    time.sleep(0.1)
print("Warm-up complete.")

# Initialize RTAB-Map
rtabmap_process.setParameter("Mem/IncrementalMemory", "true")
rtabmap_process.setParameter("Mem/InitWMWithAllNodes", "true")
rtabmap_process.init()

try:
    while True:
        frames = pipeline.wait_for_frames()
        
        aligned_frames = align.process(frames)
        
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        accel_frame = aligned_frames.first_or_default(rs.stream.accel)
        gyro_frame = aligned_frames.first_or_default(rs.stream.gyro)
        
        if not aligned_depth_frame or not color_frame or not accel_frame or not gyro_frame:
            continue
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # Get IMU data
        accel_data = accel_frame.as_motion_frame().get_motion_data()
        gyro_data = gyro_frame.as_motion_frame().get_motion_data()
        
        # Create RTAB-Map sensor data
        timestamp = time.time()
        rgbd_image = rtab.RGBDImage.create(color_image, depth_image, timestamp)
        imu_data = rtab.IMU.create([accel_data.x, accel_data.y, accel_data.z],
                                   [gyro_data.x, gyro_data.y, gyro_data.z], timestamp)
        
        # Process the data with RTAB-Map
        rtabmap_process.process(rgbd_image, imu_data)
        
        # Optionally, you can retrieve and visualize the 3D map here
        
        # Break the loop with a condition if needed (e.g., key press or specific number of frames)

finally:
    pipeline.stop()
    rtabmap_process.close()

print("SLAM processing complete.")
