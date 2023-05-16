import serial
import utm
import plotly.graph_objs as go
import plotly

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

emlid = serial.Serial('COM7', 57600, timeout=.1)
arduino = serial.Serial('COM9', 9600, timeout=.1)

origin_set = False
origin_x, origin_y = 0, 0

x_data = []
y_data = []
z_data = []

while True:
    data = emlid.readline().decode('ascii', errors='replace')
    parsed_data = parse_nmea_data(data)
    if parsed_data:
        distance = arduino.readline()[:-1].decode('ascii', errors='replace')
        if distance < 200:
            d = float(distance)
        time_utc, lat, lon = parsed_data
        print(f"[Rover] Time: {time_utc}, Lat: {lat}, Lon: {lon}, Dist: {d} cm")

        x, y, _, _ = utm.from_latlon(lat, lon)

        if not origin_set:
            origin_x, origin_y = x, y
            origin_set = True

        rel_x = x - origin_x
        rel_y = y - origin_y

        x_data.append(rel_x)
        y_data.append(rel_y)
        z_data.append(d)

        trace = go.Scatter3d(x=x_data, y=y_data, z=z_data, mode='markers', marker=dict(size=5, color=z_data, colorscale='Viridis', opacity=0.8))
        data = [trace]
        layout = go.Layout(scene=dict(xaxis_title='Distance X (m)', yaxis_title='Distance Y (m)', zaxis_title='Distance (cm)'), margin=dict(l=0, r=0, b=0, t=0))
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='map.html', auto_open=False)
