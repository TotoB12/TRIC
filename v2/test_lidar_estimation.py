import serial
from rplidar import RPLidar
import numpy as np

LIDAR_PORT = 'COM3'
SENSOR_TILT = 37.5
SENSOR_HEIGHT = 845
LIDAR_MAX_ANGLE = 1

def print_lidar_readings():
    lidar = RPLidar(LIDAR_PORT)
    try:
        print("Starting to print LIDAR readings. Press Ctrl+C to stop.")
        for measurement in lidar.iter_measures():
            if 0 <= measurement[2] <= LIDAR_MAX_ANGLE or 360 - LIDAR_MAX_ANGLE <= measurement[2] <= 360:
                delta_y = SENSOR_HEIGHT - measurement[3] * np.sin(np.deg2rad(SENSOR_TILT)) * np.cos(np.deg2rad(measurement[2]))
                d_forward = measurement[3] * np.cos(np.deg2rad(SENSOR_TILT))
                d_lateral = d_forward * np.tan(np.deg2rad(measurement[2]))
                x = np.sqrt(d_forward**2 + d_lateral**2)
                print("Elevation difference:", delta_y, "Horizontal distance:", x)
    except KeyboardInterrupt:
        print("Stopping LIDAR readings...")
    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        print("LIDAR disconnected.")

if __name__ == "__main__":
    print_lidar_readings()
