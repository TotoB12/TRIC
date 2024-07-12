import pyrealsense2 as rs
import time

pipeline = rs.pipeline()
config = rs.config()
l = 848
h = 480
fps = 30
config.enable_stream(rs.stream.depth, l, h, rs.format.z16, fps)
config.enable_stream(rs.stream.color, l, h, rs.format.bgr8, fps)

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames(timeout_ms=5000)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        print("New scan received at", time.ctime())
        # print("Depth frame:", depth_frame)

        # time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped listening to new scans.")

finally:
    pipeline.stop()
