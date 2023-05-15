import serial

port = 'COM7'
baud_rate = 57600

ser = serial.Serial(port, baud_rate)

while True:
    data = ser.readline().decode('ascii', errors='replace')
    print(data)