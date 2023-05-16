import serial

arduino = serial.Serial('COM9', 9600, timeout=.1)

while True:
	data = arduino.readline()[:-1].decode('ascii', errors='replace') #gets rid of the new-line chars
	if data:
		print(data)