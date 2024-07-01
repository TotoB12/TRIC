import serial
# from rplidar import RPLidar

a1_ser, em_ser = "COM3", "COM4"
# COM 9 ''' ulr_ard || COM7 ''' /dev/gps_tail
# lidar = RPLidar('COM3')

while True:
    with serial.Serial(a1_ser, 115200, timeout=.1) as a1:
        data = a1.readline().strip().decode("utf-8")
        print(data)
# info = lidar.get_info()
# print(info)

# health = lidar.get_health()
# print(health)

# for i, scan in enumerate(lidar.iter_scans()):
#     print('%d: Got %d measurments' % (i, len(scan)))
#     if i > 10:
#         break

# lidar.stop()
# lidar.stop_motor()
# lidar.disconnect()