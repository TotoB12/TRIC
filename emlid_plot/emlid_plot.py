import serial
import matplotlib.pyplot as plt

def dms_to_decimal(dms, direction):
    degrees, minutes = dms[:2], dms[2:]
    decimal = float(degrees) + float(minutes) / 60
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def parse_nmea_data(data):
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNGGA":
        time_utc = data[1][:2] + ":" + data[1][2:4] + ":" + data[1][4:]
        lat = dms_to_decimal(data[2], data[3])
        lon = dms_to_decimal(data[4], data[5])
        return time_utc, lat, lon

plt.ion()
origin_set = False
origin_lat = 0
origin_lon = 0

emlid = serial.Serial('COM7', 57600)

while True:
    data = emlid.readline().decode('ascii', errors='replace')
    parsed_data = parse_nmea_data(data)
    if parsed_data:
        time_utc, lat, lon = parsed_data
        if not origin_set:
            origin_lat = lat
            origin_lon = lon
            origin_set = True
        plt.scatter(lon - origin_lon, lat - origin_lat, color='green', marker='o')
        plt.pause(0.1)