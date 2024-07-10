import serial
import time
import os
import numpy as np
import plotly.graph_objs as go
import utm
import pyrealsense2 as rs
from scipy.spatial.transform import Rotation

GPS_PORT = 'COM4'
GPS_BAUD_RATE = 57600
SENSOR_HEIGHT = 0.973  # m
SENSOR_TILT = 35  # Degrees
ANGLE_FROM_GPS = 0  # Degrees
DISTANCE_FROM_GPS = 0  # m
SENSOR_ORIENTATION = 0  # Degrees
MAX_DISTANCE_FROM_SENSOR = 5.0

class DataRecorder:
    def __init__(self):
        self.gps_ser = serial.Serial(GPS_PORT, GPS_BAUD_RATE, timeout=1)
        self.start_time = time.time()
        self.session_folder = f"data_{time.strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.session_folder, exist_ok=True)
        self.gps_file = open(os.path.join(self.session_folder, 'gps_data.txt'), 'w')
        self.pointcloud_file = open(os.path.join(self.session_folder, 'pointcloud_data.npy'), 'wb')
        self.processed_file = open(os.path.join(self.session_folder, 'processed_data.txt'), 'w')
        self.current_position = None
        self.last_direction = 0
        self.gps_history = []
        
        # RealSense setup
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
        self.profile = self.pipeline.start(config)
        self.align = rs.align(rs.stream.color)
        self.pc = rs.pointcloud()
        self.latest_pointcloud = None

    def parse_nmea_data(self, data):
        data = data.strip().split(',')
        data_type = data[0][1:]

        if data_type == "GNGGA":
            try:
                lat = float(data[2][:2]) + float(data[2][2:]) / 60
                if data[3] == 'S':
                    lat = -lat
                lon = float(data[4][:3]) + float(data[4][3:]) / 60
                if data[5] == 'W':
                    lon = -lon
                return lat, lon
            except ValueError:
                return None

        elif data_type == "GNRMC" and data[8]:
            print("Direction changed:", data[8])
            self.last_direction = float(data[8])

        return None

    def record_gps(self):
        if self.gps_ser.in_waiting:
            line = self.gps_ser.readline().decode('ascii', errors='ignore')
            parsed_data = self.parse_nmea_data(line)
            if isinstance(parsed_data, tuple) and len(parsed_data) == 2:
                lat, lon = parsed_data
                timestamp = time.time() - self.start_time
                # self.current_position = (lat, lon)
                self.current_position = (37.7749, -122.4194)
                self.gps_history.append((timestamp, (lat, lon)))
                self.gps_file.write(f"{timestamp},{lat},{lon},{self.last_direction}\n")
                self.gps_file.flush()

                if len(self.gps_history) > 10:
                    self.gps_history.pop(0)

                # Save the latest pointcloud when we get a new GPS position
                if self.latest_pointcloud is not None:
                    print(f"Saving pointcloud at {timestamp:.2f} seconds.")
                    self.save_pointcloud(self.latest_pointcloud, timestamp)

    def capture_pointcloud(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        
        if not depth_frame:
            return None

        points = self.pc.calculate(depth_frame)
        vtx = np.asanyarray(points.get_vertices())
        filtered_vtx = [v for v in vtx if np.sqrt(v[0]**2 + v[1]**2 + v[2]**2) <= MAX_DISTANCE_FROM_SENSOR]
        self.latest_pointcloud = np.array([(v[0], v[1], v[2]) for v in filtered_vtx])
        print(f"Number of points in original cloud: {len(self.latest_pointcloud)}")
        return self.latest_pointcloud

    def save_pointcloud(self, pointcloud, timestamp):
        np.save(self.pointcloud_file, {'timestamp': timestamp, 'points': pointcloud})
        self.pointcloud_file.flush()

    def process_pointcloud(self, pointcloud, gps_position):
        lat, lon = gps_position
        easting, northing, _, _ = utm.from_latlon(lat, lon)

        # Create rotation matrices
        R_tilt = Rotation.from_euler('x', SENSOR_TILT, degrees=True).as_matrix()
        R_orientation = Rotation.from_euler('z', SENSOR_ORIENTATION + self.last_direction, degrees=True).as_matrix()
        R = R_orientation @ R_tilt

        # Apply rotation and translation
        transformed_points = (R @ pointcloud.T).T
        transformed_points[:, 0] += DISTANCE_FROM_GPS * np.sin(np.radians(ANGLE_FROM_GPS + self.last_direction))
        transformed_points[:, 1] += DISTANCE_FROM_GPS * np.cos(np.radians(ANGLE_FROM_GPS + self.last_direction))
        transformed_points[:, 2] += SENSOR_HEIGHT

        # Convert to UTM coordinates
        transformed_points[:, 0] += easting
        transformed_points[:, 1] += northing

        print("Processed pointcloud:")

        return transformed_points

    def close(self):
        print("Closing connections and files...")
        self.gps_ser.close()
        self.pipeline.stop()
        self.gps_file.close()
        self.pointcloud_file.close()
        self.processed_file.close()
        print("All connections and files closed.")

    def record_data(self):
        try:
            print("Recording data... Press Ctrl+C to stop.")
            while True:
                self.record_gps()
                pointcloud = self.capture_pointcloud()
                if pointcloud is not None and self.current_position is not None:
                    processed_points = self.process_pointcloud(pointcloud, self.current_position)
                    for point in processed_points:
                        self.processed_file.write(f"{point[0]},{point[1]},{point[2]}\n")
                    self.processed_file.flush()

        except KeyboardInterrupt:
            print("Stopping data recording...")
        finally:
            self.close()

def plot_data(data_folder):
    print("Plotting data...")
    try:
        processed_data = np.loadtxt(os.path.join(data_folder, 'processed_data.txt'), delimiter=',')

        if processed_data.size == 0 or processed_data.ndim == 1:
            print("Insufficient data for plotting.")
            return

        x, y, z = processed_data[:, 0], processed_data[:, 1], processed_data[:, 2]

        # Downsample for plotting
        downsample_factor = len(x) // 100000 + 1  # Aim for about 100,000 points
        x = x[::downsample_factor]
        y = y[::downsample_factor]
        z = z[::downsample_factor]

        x_rel = x - np.min(x)
        y_rel = y - np.min(y)

        x_range = np.ptp(x_rel)
        y_range = np.ptp(y_rel)
        z_range = np.ptp(z)
        
        max_range = max(x_range, y_range)
        z_scale = max_range / z_range * 0.1  # Adjust the factor as needed 

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
                colorbar=dict(title='Elevation (mm)')
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

        print(f"Plots saved in {data_folder}")
    except Exception as e:
        print(f"An error occurred while plotting: {str(e)}")

def main():
    key = input("Enter 'R' to record new data, 'P' to plot existing data, or 'Q' to quit: ").upper()
    
    if key == 'R':
        recorder = DataRecorder()
        recorder.record_data()
        
        if os.path.getsize(os.path.join(recorder.session_folder, 'processed_data.txt')) > 0:
            plot_data(recorder.session_folder)
        else:
            print("No data was recorded. Unable to generate plots.")

    elif key == 'P':
        folder = input("Enter the path to the data folder: ")
        if os.path.exists(folder):
            plot_data(folder)
        else:
            print("Invalid folder path.")

    elif key == 'Q':
        pass
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
