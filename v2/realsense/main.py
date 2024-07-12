import serial
import time
import os
import numpy as np
import plotly.graph_objs as go
import utm
import pyrealsense2 as rs
from scipy.spatial.transform import Rotation
import threading
from queue import Queue
import logging
import queue

GPS_PORT = 'COM4'
GPS_BAUD_RATE = 57600
SENSOR_HEIGHT = 0.973  # meters
SENSOR_TILT = 0  # Degrees
ANGLE_FROM_GPS = 0  # Degrees
DISTANCE_FROM_GPS = 0  # meters
SENSOR_ORIENTATION = 0  # Degrees
MAX_DISTANCE_FROM_SENSOR = 4  # meters

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DataRecorder:
    def __init__(self):
        self.start_time = time.time()
        self.session_folder = f"data_{time.strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.session_folder, exist_ok=True)
        self.gps_file = open(os.path.join(self.session_folder, 'gps_data.txt'), 'w')
        self.pointcloud_file = open(os.path.join(self.session_folder, 'pointcloud_data.npy'), 'wb')
        self.processed_file = open(os.path.join(self.session_folder, 'processed_data.txt'), 'w')
        self.performance_file = open(os.path.join(self.session_folder, 'performance_data.txt'), 'w')
        
        self.latest_pointcloud = None
        self.latest_gps = None
        self.current_heading = 0
        self.pointcloud_lock = threading.Lock()
        self.gps_lock = threading.Lock()
        self.processing_queue = Queue()
        
        self.gps_thread = threading.Thread(target=self.gps_loop)
        self.realsense_thread = threading.Thread(target=self.realsense_loop)
        self.pipeline = None
        self.align = None
        self.pipeline_started = False
        self.pipeline_lock = threading.Lock()
        self.processing_thread = threading.Thread(target=self.processing_loop)
        
        self.stop_event = threading.Event()

        # Performance monitoring
        self.total_processing_time = 0
        self.total_processed_frames = 0
        self.min_processing_time = float('inf')
        self.max_processing_time = 0

    def start(self):
        try:
            self.gps_thread.start()
            self.realsense_thread.start()
            self.processing_thread.start()
            logging.info("All threads started successfully.")
        except Exception as e:
            logging.error(f"Error starting threads: {str(e)}")
            self.stop()

    def stop(self):
        self.stop_event.set()
        for thread in [self.gps_thread, self.realsense_thread, self.processing_thread]:
            if thread.is_alive():
                thread.join()
        self.close()

    def gps_loop(self):
        try:
            gps_ser = serial.Serial(GPS_PORT, GPS_BAUD_RATE, timeout=1)
            logging.info("GPS connection established.")
        except serial.SerialException as e:
            logging.error(f"Unable to open GPS port: {str(e)}")
            self.stop_event.set()
            return

        while not self.stop_event.is_set():
            try:
                if gps_ser.in_waiting:
                    line = gps_ser.readline().decode('ascii', errors='ignore')
                    parsed_data = self.parse_nmea_data(line)
                    if parsed_data:
                        timestamp, lat, lon, heading = parsed_data
                        if heading is not None:
                            self.current_heading = heading
                        if lat is not None and lon is not None:
                            with self.gps_lock:
                                self.latest_gps = (timestamp, lat, lon, self.current_heading)
                            self.gps_file.write(f"{timestamp},{lat},{lon},{self.current_heading}\n")
                            self.gps_file.flush()
                            self.processing_queue.put(('gps', (timestamp, lat, lon, self.current_heading)))
            except serial.SerialException as e:
                logging.error(f"GPS read error: {str(e)}")
                self.stop_event.set()
                break
        
        gps_ser.close()

    def realsense_loop(self):
        try:
            self.pipeline = rs.pipeline()
            config = rs.config()
            config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
            config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
            
            with self.pipeline_lock:
                self.pipeline.start(config)
                self.pipeline_started = True
            
            self.align = rs.align(rs.stream.color)
            
            logging.info("RealSense camera initialized successfully.")
        except rs.error as e:
            logging.error(f"Failed to initialize RealSense camera: {str(e)}")
            self.stop_event.set()
            return

        try:
            while not self.stop_event.is_set():
                frames = self.pipeline.wait_for_frames()
                aligned_frames = self.align.process(frames)
                
                depth_frame = aligned_frames.get_depth_frame()
                color_frame = aligned_frames.get_color_frame()
                
                if not depth_frame or not color_frame:
                    continue
                
                pc = rs.pointcloud()
                pc.map_to(color_frame)
                points = pc.calculate(depth_frame)
                
                vtx = np.asanyarray(points.get_vertices())
                pointcloud = np.array([(v[0], v[1], v[2]) for v in vtx])
                
                with self.pointcloud_lock:
                    self.latest_pointcloud = pointcloud
                                
        except rs.error as e:
            logging.error(f"RealSense camera error: {str(e)}")
        finally:
            self.stop_pipeline()

    def stop_pipeline(self):
        with self.pipeline_lock:
            if self.pipeline and self.pipeline_started:
                try:
                    self.pipeline.stop()
                    self.pipeline_started = False
                    logging.info("RealSense pipeline stopped successfully.")
                except Exception as e:
                    logging.error(f"Error stopping RealSense pipeline: {str(e)}")

    def processing_loop(self):
        while not self.stop_event.is_set():
            try:
                item = self.processing_queue.get(timeout=1)
                if item[0] == 'gps':
                    process_start_time = time.time()
                    timestamp, lat, lon, heading = item[1]
                    with self.pointcloud_lock:
                        if self.latest_pointcloud is not None:
                            np.save(self.pointcloud_file, {'timestamp': timestamp, 'points': self.latest_pointcloud})
                            self.pointcloud_file.flush()
                            processed_points = self.process_pointcloud(self.latest_pointcloud, (lat, lon, heading))
                            for point in processed_points:
                                self.processed_file.write(f"{timestamp},{point[0]},{point[1]},{point[2]}\n")
                            self.processed_file.flush()
                            process_end_time = time.time()
                            processing_time = process_end_time - process_start_time
                            total_time = process_end_time - timestamp
                            self.log_performance(timestamp, processing_time, total_time)
                            logging.info(f"Processed and saved data for timestamp {timestamp}")
                self.processing_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Error in processing loop: {str(e)}")
                if self.stop_event.is_set():
                    break

    def parse_nmea_data(self, data):
        data = data.strip().split(',')
        data_type = data[0][1:]

        if data_type == "GNGGA":
            try:
                timestamp = time.time() - self.start_time
                lat = float(data[2][:2]) + float(data[2][2:]) / 60
                if data[3] == 'S':
                    lat = -lat
                lon = float(data[4][:3]) + float(data[4][3:]) / 60
                if data[5] == 'W':
                    lon = -lon
                return timestamp, lat, lon, None
            except (ValueError, IndexError):
                logging.warning(f"Invalid GNGGA data: {data}")
                return None
        elif data_type == "GNRMC":
            try:
                timestamp = time.time() - self.start_time
                heading = float(data[8]) if data[8] else None
                return timestamp, None, None, heading
            except (ValueError, IndexError):
                logging.warning(f"Invalid GNRMC data: {data}")
                return None

        return None

    def process_pointcloud(self, pointcloud, gps_data):
        voxel_size = 0.05  # 5cm voxel size
        voxel_grid = {}
        for point in pointcloud:
            voxel_key = tuple(np.floor(point / voxel_size).astype(int))
            if voxel_key not in voxel_grid or point[2] < voxel_grid[voxel_key][2]:
                voxel_grid[voxel_key] = point
        downsampled_pointcloud = np.array(list(voxel_grid.values()))

        lat, lon, heading = gps_data
        easting, northing, _, _ = utm.from_latlon(lat, lon)

        R_tilt = Rotation.from_euler('x', SENSOR_TILT-90, degrees=True).as_matrix()
        R_orientation = Rotation.from_euler('z', SENSOR_ORIENTATION + heading, degrees=True).as_matrix()
        R = R_orientation @ R_tilt

        transformed_points = (R @ downsampled_pointcloud.T).T
        transformed_points[:, 0] += DISTANCE_FROM_GPS * np.sin(np.radians(ANGLE_FROM_GPS + heading))
        transformed_points[:, 1] += DISTANCE_FROM_GPS * np.cos(np.radians(ANGLE_FROM_GPS + heading))
        transformed_points[:, 2] += SENSOR_HEIGHT

        distances = np.linalg.norm(transformed_points, axis=1)
        transformed_points = transformed_points[distances <= MAX_DISTANCE_FROM_SENSOR]

        transformed_points[:, 0] += easting
        transformed_points[:, 1] += northing

        return transformed_points

    def log_performance(self, timestamp, processing_time, total_time):
        self.total_processing_time += processing_time
        self.total_processed_frames += 1
        self.min_processing_time = min(self.min_processing_time, processing_time)
        self.max_processing_time = max(self.max_processing_time, processing_time)
        
        avg_processing_time = self.total_processing_time / self.total_processed_frames
        
        performance_log = (f"Timestamp: {timestamp:.3f}, "
                           f"Processing Time: {processing_time:.3f}s, "
                           f"Total Time: {total_time:.3f}s, "
                           f"Avg Processing Time: {avg_processing_time:.3f}s, "
                           f"Min Processing Time: {self.min_processing_time:.3f}s, "
                           f"Max Processing Time: {self.max_processing_time:.3f}s\n")
        
        self.performance_file.write(performance_log)
        self.performance_file.flush()
        
        logging.debug(performance_log.strip())

    def close(self):
        logging.info("Closing connections and files...")
        self.stop_pipeline()
        self.gps_file.close()
        self.pointcloud_file.close()
        self.processed_file.close()
        self.performance_file.close()
        logging.info("All connections and files closed.")

def plot_data(data_folder):
    logging.info("Plotting data...")
    try:
        processed_data = np.loadtxt(os.path.join(data_folder, 'processed_data.txt'), delimiter=',')

        if processed_data.size == 0 or processed_data.ndim == 1:
            logging.warning("Insufficient data for plotting.")
            return

        timestamps, x, y, z = processed_data[:, 0], processed_data[:, 1], processed_data[:, 2], processed_data[:, 3]

        x_rel = x - np.min(x)
        y_rel = y - np.min(y)

        fig_3d = go.Figure(data=[go.Scatter3d(
            x=x_rel,
            y=y_rel,
            z=z,
            mode='markers',
            marker=dict(
                size=3,
                color=z,
                colorscale='Viridis',
                opacity=1,
                colorbar=dict(title='Elevation (m)')
            )
        )])

        fig_3d.update_layout(
            scene=dict(
                aspectmode='data',
                xaxis_title='Relative Easting (m)',
                yaxis_title='Relative Northing (m)',
                zaxis_title='Elevation (m)'
            ),
            title='3D Point Cloud'
        )

        fig_3d.write_html(os.path.join(data_folder, '3d_pointcloud.html'))

        fig_2d = go.Figure(data=[go.Scatter(
            x=x_rel,
            y=y_rel,
            mode='markers',
            marker=dict(
                size=3,
                color=z,
                colorscale='Viridis',
                opacity=1,
                colorbar=dict(title='Elevation (m)')
            )
        )])

        fig_2d.update_layout(
            xaxis_title='Relative Easting (m)',
            yaxis_title='Relative Northing (m)',
            title='2D Point Cloud Projection'
        )

        fig_2d.write_html(os.path.join(data_folder, '2d_pointcloud.html'))

        logging.info(f"Plots saved in {data_folder}")
    except Exception as e:
        logging.error(f"An error occurred while plotting: {str(e)}")

def main():
    while True:
        key = input("Enter 'R' to record new data, 'P' to plot existing data, or 'Q' to quit: ").upper()
        
        if key == 'R':
            recorder = DataRecorder()
            try:
                recorder.start()
                input("Press Enter to stop recording...\n")
            except Exception as e:
                logging.error(f"Error during recording: {str(e)}")
            finally:
                recorder.stop()
            
            if os.path.exists(recorder.session_folder) and os.path.getsize(os.path.join(recorder.session_folder, 'processed_data.txt')) > 0:
                plot_data(recorder.session_folder)
            else:
                logging.warning("No data was recorded or the data file is empty. Unable to generate plots.")

        elif key == 'P':
            folder = input("Enter the path to the data folder: ")
            if os.path.exists(folder):
                plot_data(folder)
            else:
                logging.error("Invalid folder path.")

        elif key == 'Q':
            break
        else:
            logging.warning("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
