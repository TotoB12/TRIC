import serial

arduino = serial.Serial('COM3', 9600, timeout=.1)

while True:
	if data := arduino.readline()[:-1].decode('ascii', errors='replace'):
		print(data)
