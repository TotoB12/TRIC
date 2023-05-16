import serial
import matplotlib.pyplot as plt
import utm

def parse_nmea_data(data):
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNGGA":
        time_utc = data[1][:2] + ":" + data[1][2:4] + ":" + data[1][4:]
        try:
            lat = float(data[2][:2]) + float(data[2][2:]) / 60
            if data[3] == 'S':
                lat = -lat
            lon = float(data[4][:3]) + float(data[4][3:]) / 60
            if data[5] == 'W':
                lon = -lon
        except ValueError:
            print("bad data")
            return None

        return time_utc, lat, lon

emlid = serial.Serial('COM7', 57600)

plt.ion()
fig, ax = plt.subplots()

origin_set = False
origin_x, origin_y = 0, 0

while True:
    data = emlid.readline().decode('ascii', errors='replace')
    parsed_data = parse_nmea_data(data)
    if parsed_data:
        time_utc, lat, lon = parsed_data
        print(f"[Plot] Time: {time_utc}, Lat: {lat}, Lon: {lon}")

        x, y, _, _ = utm.from_latlon(lat, lon)

        if not origin_set:
            origin_x, origin_y = x, y
            origin_set = True

        rel_x = x - origin_x
        rel_y = y - origin_y

        ax.scatter(rel_x, rel_y, c='green', marker='o')
        plt.draw()
        plt.pause(0.01)