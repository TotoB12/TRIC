import serial
import utm
import plotly.graph_objs as go
import plotly
import os
import time
import numpy as np
from rplidar import RPLidar
import threading

# Constants
GPS_PORT = 'COM4'
LIDAR_PORT = 'COM3'
GPS_BAUD = 11520
LIDAR_MAX_ANGLE = 45  # Maximum angle to consider on each side
SENSOR_HEIGHT = 1000  # Height of the LIDAR sensor from the ground in mm
SENSOR_TILT = 56  # Downward tilt of the LIDAR sensor in degrees

# Global variables
gps_data = {'time': None, 'lat': None, 'lon': None, 'direction': None}
lidar_data = []
start_time = None
folder_name = None

def parse_nmea_data(data):
    global start_time, folder_name
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNZDA":
        date = f"{data[4]}-{data[3]}-{data[2]}"
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}"
        if start_time is None:
            start_time = time_utc
            folder_name = time_utc.replace(':', '-')
            os.makedirs(f"data/{folder_name}", exist_ok=True)
        return time_utc

    if data_type == "GNGGA" and start_time is not None:
        time_utc = f"{start_time[:10]}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}"
        try:
            lat = float(data[2][:2]) + float(data[2][2:]) / 60
            if data[3] == 'S':
                lat = -lat
            lon = float(data[4][:3]) + float(data[4][3:]) / 60
            if data[5] == 'W':
                lon = -lon
            gps_data['time'] = time_utc
            gps_data['lat'] = lat
            gps_data['lon'] = lon
        except ValueError:
            print("Bad GPS data")

    if data_type == "GNRMC" and start_time is not None:
        if data[8] != '':
            gps_data['direction'] = float(data[8])

def gps_thread():
    with serial.Serial(GPS_PORT, GPS_BAUD, timeout=1) as gps_ser:
        while True:
            if gps_ser.in_waiting > 0:
                data = gps_ser.readline().decode('ascii', errors='replace')
                parse_nmea_data(data)

def calculate_point_location(distance, angle):
    # Convert angles to radians
    alpha = np.deg2rad(SENSOR_TILT)
    beta = np.deg2rad(angle)

    # Calculate elevation difference
    delta_y = SENSOR_HEIGHT - distance * np.sin(alpha) * np.cos(beta)

    # Calculate horizontal distance
    d_forward = distance * np.cos(alpha)
    d_lateral = d_forward * np.tan(beta)
    x = np.sqrt(d_forward**2 + d_lateral**2)

    return x, delta_y

def lidar_thread():
    lidar = RPLidar(LIDAR_PORT)
    try:
        for measurement in lidar.iter_measures():
            quality, angle, distance = measurement[1], measurement[2], measurement[3]
            if quality > 0 and -LIDAR_MAX_ANGLE <= angle <= LIDAR_MAX_ANGLE:
                x, y = calculate_point_location(distance, angle)
                lidar_data.append((time.time(), angle, distance, x, y))
    except KeyboardInterrupt:
        pass
    finally:
        lidar.stop()
        lidar.disconnect()

def save_data():
    gps_file = open(f"data/{folder_name}/gps_data.txt", 'w')
    lidar_file = open(f"data/{folder_name}/lidar_data.txt", 'w')
    processed_file = open(f"data/{folder_name}/processed_data.txt", 'w')

    last_gps_time = None
    for lidar_time, angle, distance, x, y in lidar_data:
        if gps_data['time'] != last_gps_time:
            gps_file.write(f"{gps_data['time']},{gps_data['lat']},{gps_data['lon']},{gps_data['direction']}\n")
            last_gps_time = gps_data['time']

        lidar_file.write(f"{lidar_time},{angle},{distance}\n")

        if gps_data['lat'] is not None and gps_data['lon'] is not None and gps_data['direction'] is not None:
            utm_x, utm_y, _, _ = utm.from_latlon(gps_data['lat'], gps_data['lon'])
            direction_rad = np.deg2rad(gps_data['direction'])
            point_x = utm_x + x * np.sin(direction_rad)
            point_y = utm_y + x * np.cos(direction_rad)
            processed_file.write(f"{lidar_time},{point_x},{point_y},{y}\n")

    gps_file.close()
    lidar_file.close()
    processed_file.close()

def plot_data(file_path):
    x_data, y_data, z_data = [], [], []
    with open(file_path, 'r') as f:
        for line in f:
            _, x, y, z = line.strip().split(',')
            x_data.append(float(x))
            y_data.append(float(y))
            z_data.append(float(z))

    # 3D Surface Plot
    trace1 = go.Scatter3d(x=x_data, y=y_data, z=z_data, mode='markers', marker=dict(size=2, color=z_data, colorscale='Viridis', opacity=0.8))
    layout1 = go.Layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Elevation'))
    fig1 = go.Figure(data=[trace1], layout=layout1)
    plotly.offline.plot(fig1, filename=f"data/{folder_name}/3d_plot.html", auto_open=False)

    # 2D Elevation Heatmap
    trace2 = go.Heatmap(x=x_data, y=y_data, z=z_data, colorscale='Viridis')
    layout2 = go.Layout(title='Elevation Heatmap', xaxis_title='X', yaxis_title='Y')
    fig2 = go.Figure(data=[trace2], layout=layout2)
    plotly.offline.plot(fig2, filename=f"data/{folder_name}/2d_heatmap.html", auto_open=False)

def main():
    choice = input("Enter 1 to start a new recording session, or 2 to plot from an existing file: ")

    if choice == '1':
        gps_thread = threading.Thread(target=gps_thread)
        lidar_thread = threading.Thread(target=lidar_thread)

        gps_thread.start()
        lidar_thread.start()

        print("Recording data. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping recording and saving data...")

        save_data()
        plot_data(f"data/{folder_name}/processed_data.txt")
        print("Data saved and plots generated.")

    elif choice == '2':
        file_path = input("Enter the path to the processed data file: ")
        plot_data(file_path)
        print("Plots generated.")

    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()