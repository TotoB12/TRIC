import serial
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2

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
    
def distance_between_points(lat1, lon1, lat2, lon2):
    R = 6371.01  # Approximate radius of earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c * 1000  # Convert to meters
    return distance

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
        distance = distance_between_points(lat, lon, origin_lat, origin_lon)
        plt.scatter(distance, color='green', marker='o')
        plt.pause(0.1)  
