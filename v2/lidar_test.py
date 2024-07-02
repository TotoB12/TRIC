import sys
from rplidar import RPLidar

PORT_NAME = 'COM3'

def record_measurements(path):
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')
    try:
        print('Recording measurements... Press Crl+C to stop.')
        for measurement in lidar.iter_measures():
            if measurement[1] > 0:
                line = '\t'.join(str(v) for v in measurement)
                outfile.write(line + '\n')
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    outfile.close()

if __name__ == '__main__':
    record_measurements("out.txt")
