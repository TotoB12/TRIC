import serial
from flask import Flask, render_template

app = Flask(__name__)

live_data = ""

def parse_nmea_data(data):
    data = data.strip().split(',')
    data_type = data[0][1:]

    if data_type == "GNGGA":
        time_utc = data[1][:2] + ":" + data[1][2:4] + ":" + data[1][4:]
        lat = data[2][:2] + "°" + data[2][2:] + "'" + data[3]
        lon = data[4][:3] + "°" + data[4][3:] + "'" + data[5]
        return f"[Rover] Time: {time_utc}, Lat: {lat}, Lon: {lon}"

emlid = serial.Serial('COM7', 11520, timeout=.1)
arduino = serial.Serial('COM9', 9600, timeout=.1)

def update_live_data():
    global live_data
    while True:
        if arduino.in_waiting > 0:
            ar_data = arduino.readline()[:-1].decode('ascii', errors='replace')
            if ar_data:
                d = ar_data

        if emlid.in_waiting > 0:
            em_data = emlid.readline().decode('ascii', errors='replace')
            em_parsed_data = parse_nmea_data(em_data)
            data = f'{em_parsed_data}, Dist: {d} cm'
            if em_parsed_data:
                live_data = data

from threading import Thread
t = Thread(target=update_live_data)
t.start()

@app.route('/')
def index():
    global live_data
    return render_template('index.html', live_data=live_data)

if __name__ == '__main__':
    app.run(debug=True)
