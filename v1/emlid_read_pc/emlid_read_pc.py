# import serial

# port = 'COM7'
# baud_rate = 57600

# ser = serial.Serial(port, baud_rate)

# while True:
#     data = ser.readline().decode('ascii', errors='replace')
#     print(data)

import serial

choice = input("Full (f) or Clean (c): ")

def parse_nmea_data(data):
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNGGA":
        time_utc = data[1][:2] + ":" + data[1][2:4] + ":" + data[1][4:]
        lat = data[2][:2] + "°" + data[2][2:] + "'" + data[3]
        lon = data[4][:3] + "°" + data[4][3:] + "'" + data[5]
        fix_quality = data[6]
        num_satellites = data[7]
        altitude = data[9] + "m"
        return f"[Plot] Time: {time_utc}, Lat: {lat}, Lon: {lon}, Fix Quality: {fix_quality}, Satellites Used: {num_satellites}, Altitude: {altitude}"
    if data_type == "GNEBP":
        base_lat = f"{data[1][:2]}°{data[1][2:]}'{data[2]}"
        base_lon = f"{data[3][:3]}°{data[3][3:]}'{data[4]}"
        base_altitude = f"{data[5]}m"
        return f"[Base] Lat: {base_lat}, Lon: {base_lon}, Altitude: {base_altitude}"

emlid = serial.Serial('COM4', 57600)
if choice == "c":
    while True:
        data = emlid.readline().decode('ascii', errors='replace')
        if parsed_data := parse_nmea_data(data):
            print(parsed_data)
if choice == "f":
    while True:
        data = emlid.readline().decode('ascii', errors='replace')
        print(data)
