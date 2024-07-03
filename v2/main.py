import serial
import time
import os
import numpy as np
import plotly.graph_objs as go
from scipy.interpolate import griddata
from rplidar import RPLidar
import utm
import math

# Constants and Configuration
GPS_PORT = 'COM4'
LIDAR_PORT = 'COM3'
GPS_BAUD_RATE = 11520
LIDAR_MAX_ANGLE = 30  # Degrees to each side
SENSOR_HEIGHT = 800  # mm
SENSOR_TILT = 56  # Degrees

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
        # elif data_type == "GNRMC":
            # self.last_direction = 0
            self.last_direction = float(data[8])

        return None

    def record_gps(self):
        if self.gps_ser.in_waiting:
            line = self.gps_ser.readline().decode('ascii', errors='ignore')
            parsed_data = self.parse_nmea_data(line)
            if isinstance(parsed_data, tuple) and len(parsed_data) == 2:
                lat, lon = parsed_data
                self.current_position = (lat, lon)
                # self.current_position = (37.7749, -122.4194)
                timestamp = time.time() - self.start_time
                self.gps_file.write(f"{timestamp},{lat},{lon},{self.last_direction}\n")
                self.gps_file.flush()

    def process_lidar_point(self, angle, distance):
        if self.current_position is None or distance == 0 or self.last_direction is None:
            return None

        if not (0 <= angle <= LIDAR_MAX_ANGLE or 360 - LIDAR_MAX_ANGLE <= angle <= 360):
            return None

        lat, lon = self.current_position

        # Calculate elevation and horizontal distance
        # The elevation difference is the vertical component of the measured distance
        delta_y = SENSOR_HEIGHT - distance * np.sin(np.deg2rad(SENSOR_TILT)) * np.cos(np.deg2rad(angle))
        d_forward = distance * np.cos(np.deg2rad(SENSOR_TILT))
        d_lateral = d_forward * np.tan(np.deg2rad(angle))
        # The horizontal distance is the horizontal component of the measured distance
        x = np.sqrt(d_forward**2 + d_lateral**2)

        print(f"Distance: {distance}, Angle: {angle}, Delta Y: {delta_y}, X: {x}")

        # Convert to UTM
        easting, northing, _, _ = utm.from_latlon(lat, lon)

        # Adjust position based on LIDAR measurement and heading
        adjusted_angle = self.last_direction + angle
        adjusted_easting = easting + x * np.sin(np.deg2rad(adjusted_angle)) / 1000
        adjusted_northing = northing + x * np.cos(np.deg2rad(adjusted_angle)) / 1000

        return adjusted_easting, adjusted_northing, delta_y

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
                
                if quality > 0 and distance > 0:
                    self.lidar_file.write(f"{timestamp},{new_scan},{quality},{angle},{distance}\n")
                    self.lidar_file.flush()

                    processed_point = self.process_lidar_point(angle, distance)
                    if processed_point:
                        self.processed_file.write(f"{processed_point[0]},{processed_point[1]},{processed_point[2]}\n")
                        self.processed_file.flush()

        except KeyboardInterrupt:
            print("Stopping data recording...")
        finally:
            self.close()

def plot_data(data_folder):
    try:
        processed_data = np.loadtxt(os.path.join(data_folder, 'processed_data.txt'), delimiter=',')
        
        if processed_data.size == 0 or processed_data.ndim == 1:
            print("Insufficient data for plotting.")
            return
        
        x, y, z = processed_data[:, 0], processed_data[:, 1], processed_data[:, 2]

        # Create a grid for the surface plot
        xi = np.linspace(min(x), max(x), 200)
        yi = np.linspace(min(y), max(y), 200)
        X, Y = np.meshgrid(xi, yi)

        # Interpolate Z values on the grid
        Z = griddata((x, y), z, (X, Y), method='linear')

        # 3D Surface Plot
        fig_3d = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
        fig_3d.update_layout(scene=dict(
            xaxis_title='Easting',
            yaxis_title='Northing',
            zaxis_title='Elevation (mm)',
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=0.5)
        ), title='3D Surface Plot')
        fig_3d.write_html(os.path.join(data_folder, '3d_surface_plot.html'))

        # 2D Elevation Heatmap
        fig_2d = go.Figure(data=go.Heatmap(x=x, y=y, z=z, colorscale='Viridis'))
        fig_2d.update_layout(
            xaxis_title='Easting',
            yaxis_title='Northing',
            title='2D Elevation Heatmap'
        )
        fig_2d.write_html(os.path.join(data_folder, '2d_heatmap.html'))

        print(f"Plots saved in {data_folder}")
    except Exception as e:
        print(f"An error occurred while plotting: {str(e)}")

def main():
    while True:
        choice = input("Enter 'R' to record new data, 'P' to plot existing data, or 'Q' to quit: ").upper()
        
        if choice == 'R':
            recorder = DataRecorder()
            recorder.record_data()
            
            if os.path.getsize(os.path.join(recorder.session_folder, 'processed_data.txt')) > 0:
                plot_data(recorder.session_folder)
            else:
                print("No data was recorded. Unable to generate plots.")
        
        elif choice == 'P':
            folder = input("Enter the path to the data folder: ")
            if os.path.exists(folder):
                plot_data(folder)
            else:
                print("Invalid folder path.")
        elif choice == 'Q':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()