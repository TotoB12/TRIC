import serial, time, keyboard

def parse_nmea_data(data):
    d = data.strip().split(',')
    t = d[0][1:]
    if t == "GNGGA":
        return f"[Rover] Time: {d[1][:2]}:{d[1][2:4]}:{d[1][4:]}, Lat: {d[2][:2]}°{d[2][2:]}'{d[3]}, Lon: {d[4][:3]}°{d[4][3:]}'{d[5]}"

emlid, arduino, ded = serial.Serial('COM8', 57600, timeout=.1), serial.Serial('COM3', 9600, timeout=.1), False
# emlid, ded = serial.Serial('COM8', 57600, timeout=.1), False

time.sleep(1)
emlid.flushInput()
arduino.flushInput()

while True:
    if arduino.in_waiting > 0:
        if ar_data := arduino.readline()[:-1].decode('ascii', errors='replace'): d, ded = ar_data, True
    if ded and emlid.in_waiting > 0:
        em_data = emlid.readline().decode('ascii', errors='replace')
        if em_parsed_data := parse_nmea_data(em_data): print(f'{em_parsed_data}, Dist: {d} cm')
    if keyboard.is_pressed('s') or keyboard.is_pressed('c'):
        break
