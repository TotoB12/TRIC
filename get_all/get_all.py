import serial

def parse_nmea_data(data):
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNGGA":
        time_utc = data[1][:2] + ":" + data[1][2:4] + ":" + data[1][4:]
        lat = data[2][:2] + "°" + data[2][2:] + "'" + data[3]
        lon = data[4][:3] + "°" + data[4][3:] + "'" + data[5]
        return f"Time: {time_utc}, Lat: {lat}, Lon: {lon}"

emlid = serial.Serial('COM7', 57600, timeout=.1)
arduino = serial.Serial('COM1', 115200, timeout=.1)

while True:
    em_data = emlid.readline().decode('ascii', errors='replace')
    em_parsed_data = parse_nmea_data(em_data)
    ar_data = arduino.readline()[:-2]
    if em_parsed_data:
        print(em_parsed_data)
    if ar_data:
        print(ar_data)
