import pyrealsense2 as rs
import time

# Setup RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
# Configure the streams; adjust according to your needs
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 6)
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 6)

# Start the pipeline
pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # print("New scan received at", time.ctime())
        print("Depth frame:", depth_frame)

        # time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped listening to new scans.")

finally:
    pipeline.stop()
