# import serial

# port = 'COM7'
# baud_rate = 57600

# ser = serial.Serial(port, baud_rate)

# while True:
#     data = ser.readline().decode('ascii', errors='replace')
#     print(data)



import serial

def parse_nmea_data(data):
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNGGA":
        time_utc = data[1][:2] + ":" + data[1][2:4] + ":" + data[1][4:]
        lat = data[2][:2] + "°" + data[2][2:] + "'" + data[3]
        lon = data[4][:3] + "°" + data[4][3:] + "'" + data[5]
        fix_quality = data[6]
        num_satellites = data[7]
        hdop = data[8]
        altitude = data[9] + "m"
        geoidal_sep = data[11] + "m"
        return f"[GNGGA] Time: {time_utc}, Lat: {lat}, Lon: {lon}, Fix Quality: {fix_quality}, Satellites: {num_satellites}, HDOP: {hdop}, Altitude: {altitude}, Geoidal Separation: {geoidal_sep}"

port = 'COM7'
baud_rate = 57600

ser = serial.Serial(port, baud_rate)

while True:
    data = ser.readline().decode('ascii', errors='replace')
    parsed_data = parse_nmea_data(data)
    if parsed_data:
        print(parsed_data)
