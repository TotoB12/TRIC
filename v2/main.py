import serial, utm, plotly.graph_objs as go, plotly, os, time, numpy as np, logging

a1_ser, em_ser = "COM3", "COM4"

print("Please wait...")
date = start_time = None

def parse_nmea_data(data):
    global date, start_time, last_direction
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNZDA":
        date = f"{data[4]}-{data[3]}-{data[2]}"
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}"
        if start_time is None:
            start_time = time_utc
            os.makedirs(f"data/{time_utc.replace(':', '-')}")
        return time_utc

    if data_type == "GNGGA" and date is not None:
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}"
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

    if data_type == "GNRMC" and date is not None:
        time_utc = f"{date}_{data[1][:2]}:{data[1][2:4]}:{data[1][4:]}"
        if data[8] != '':
            last_direction = float(data[8])

emlid = serial.Serial(em_ser, 11520, timeout=.1)
arduino = serial.Serial(ar_ser, 9600, timeout=.1)

# time.sleep(1)
emlid.flushInput()
arduino.flushInput()

origin_set, ded = False, False
origin_x, origin_y, last_direction = 0, 0, 0
x, y = 1, 1

while start_time is None:
    if emlid.in_waiting > 0:
        data = emlid.readline().decode('ascii', errors='replace')
        parse_nmea_data(data)

folder_name = start_time.replace(':', '-')
folder_path = os.path.join('data', folder_name)

while not os.path.exists(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
    except FileExistsError:
        print("Data already exists")

