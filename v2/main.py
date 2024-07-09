import serial
import time
import os
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
from rplidar import RPLidar
import utm
import math
import msvcrt

GPS_PORT = 'COM4'
LIDAR_PORT = 'COM3'
GPS_BAUD_RATE = 57600
LIDAR_MAX_ANGLE = 45  # Degrees to each side
SENSOR_HEIGHT = 803  # mm
SENSOR_TILT = 55  # Degrees
MIN_DISTANCE = 0  # mm
MIN_HEIGHT = 0  # mm
ANGLE_FROM_GPS = 0  # Degrees
DISTANCE_FROM_GPS = 0  # mm
LIDAR_ORIENTATION = 0  # Degrees

class DataRecorder:
    def __init__(self):
        self.gps_ser = serial.Serial(GPS_PORT, GPS_BAUD_RATE, timeout=1)
        self.lidar = RPLidar(LIDAR_PORT)
        self.start_time = time.time()
        self.session_folder = f"data_{time.strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.session_folder, exist_ok=True)
        self.gps_file = open(os.path.join(self.session_folder, 'gps_data.txt'), 'w')
        self.lidar_file = open(os.path.join(self.session_folder, 'lidar_data.txt'), 'w')
        self.processed_file = open(os.path.join(self.session_folder, 'processed_data.txt'), 'w')
        self.current_position = None
        self.last_direction = 0
        self.gps_history = []

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
                self.current_position = (lat, lon)
                self.gps_history.append((timestamp, (lat, lon)))
                self.gps_file.write(f"{timestamp},{lat},{lon},{self.last_direction}\n")
                self.gps_file.flush()

                if len(self.gps_history) > 10:
                    self.gps_history.pop(0)

    def process_lidar_point(self, timestamp, angle, distance):
        interpolated_position = self.interpolate_position(timestamp)
        if interpolated_position is None or distance == 0 or self.last_direction is None:
            print("Invalid data for processing.")
            return None

        adjusted_angle = (angle + LIDAR_ORIENTATION) % 360

        # if not (0 <= adjusted_angle <= LIDAR_MAX_ANGLE or 360 - LIDAR_MAX_ANGLE <= adjusted_angle <= 360):
        #     print("Angle out of range:", adjusted_angle)
        #     return None

        lat, lon = interpolated_position

        # Calculate elevation and horizontal distance
        # The elevation difference is the vertical component of the measured distance
        delta_y = SENSOR_HEIGHT - distance * np.sin(np.deg2rad(SENSOR_TILT)) * np.cos(np.deg2rad(adjusted_angle))
        d_forward = distance * np.cos(np.deg2rad(SENSOR_TILT))
        d_lateral = d_forward * np.tan(np.deg2rad(adjusted_angle))
        # The horizontal distance is the horizontal component of the measured distance
        x = np.sqrt(d_forward**2 + d_lateral**2)

        easting, northing, _, _ = utm.from_latlon(lat, lon)

        lidar_offset_angle = np.deg2rad(self.last_direction + ANGLE_FROM_GPS)
        lidar_offset_easting = DISTANCE_FROM_GPS * np.sin(lidar_offset_angle) / 1000
        lidar_offset_northing = DISTANCE_FROM_GPS * np.cos(lidar_offset_angle) / 1000

        final_angle = np.deg2rad(self.last_direction + ANGLE_FROM_GPS + adjusted_angle)
        adjusted_easting = easting + lidar_offset_easting + x * np.sin(final_angle) / 1000
        adjusted_northing = northing + lidar_offset_northing + x * np.cos(final_angle) / 1000

        # print("Adjusted Easting:", adjusted_easting, "Adjusted Northing:", adjusted_northing, "Height:", delta_y)

        return adjusted_easting, adjusted_northing, delta_y

    def interpolate_position(self, timestamp):
        if len(self.gps_history) < 2:
            return self.current_position

        for i in range(1, len(self.gps_history)):
            prev_time, prev_pos = self.gps_history[i-1]
            curr_time, curr_pos = self.gps_history[i]
            
            if prev_time <= timestamp <= curr_time:
                t = (timestamp - prev_time) / (curr_time - prev_time)
                lat = prev_pos[0] + t * (curr_pos[0] - prev_pos[0])
                lon = prev_pos[1] + t * (curr_pos[1] - prev_pos[1])
                return (lat, lon)

        return self.current_position

    def close(self):
        print("Closing connections and files...")
        self.gps_ser.close()
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()
        self.gps_file.close()
        self.lidar_file.close()
        self.processed_file.close()
        print("All connections and files closed.")

    def record_data(self):
        try:
            print("Recording data... Press Ctrl+C to stop.")
            for measurement in self.lidar.iter_measures():
                self.record_gps()
                timestamp = time.time() - self.start_time
                
                new_scan, quality, angle, distance = measurement
                
                adjusted_angle = (angle + LIDAR_ORIENTATION) % 360
                # print(adjusted_angle)
                
                # change depending on opinion
                if quality == 15 and distance > MIN_DISTANCE and (0 <= adjusted_angle <= LIDAR_MAX_ANGLE or 360 - LIDAR_MAX_ANGLE <= adjusted_angle <= 360):
                    self.lidar_file.write(f"{timestamp},{new_scan},{quality},{adjusted_angle},{distance}\n")
                    self.lidar_file.flush()
                    processed_point = self.process_lidar_point(timestamp, angle, distance)
                    if processed_point and processed_point[2] >= MIN_HEIGHT:
                        self.processed_file.write(f"{processed_point[0]},{processed_point[1]},{processed_point[2]}\n")
                        self.processed_file.flush()
                        if 0 <= adjusted_angle <= 2 or 360 - 2 <= adjusted_angle <= 360:
                            print("Height:", processed_point[2], "Angle:", adjusted_angle)

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

        x_rel = x - np.min(x)
        y_rel = y - np.min(y)

        x_range = np.ptp(x_rel)
        y_range = np.ptp(y_rel)
        z_range = np.ptp(z)
        
        max_range = max(x_range, y_range)
        z_scale = max_range / z_range * 0.1  # Adjust the factor as needed 

        fig_3d = go.Figure(data=[go.Scatter3d(
            x=x_rel,
            y=y_rel,
            z=z,
            mode='markers',
            marker=dict(
                size=7,
                color=z,
                colorscale='Balance',
                # colorscale='Viridis',
                opacity=1,
                colorbar=dict(title='Elevation (mm)')
            )
        )])
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
                size=7,
                color=z,
                colorscale='Balance',
                # colorscale='Viridis',
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
    print("Enter 'R' to record new data, 'P' to plot existing data, or 'Q' to quit: ")
    
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode().upper()
            if key == 'R':
                recorder = DataRecorder()
                recorder.record_data()
                
                if os.path.getsize(os.path.join(recorder.session_folder, 'processed_data.txt')) > 0:
                    plot_data(recorder.session_folder)
                else:
                    print("No data was recorded. Unable to generate plots.")
                break
            
            elif key == 'P':
                folder = input("Enter the path to the data folder: ")
                if os.path.exists(folder):
                    plot_data(folder)
                else:
                    print("Invalid folder path.")
                break
            
            elif key == 'Q' or key == 'C':
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
