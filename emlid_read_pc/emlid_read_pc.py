import serial

def read_nmea_messages(port, baudrate):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        while True:
            line = ser.readline().decode('ascii')
            if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                yield line.strip()

def main():
    port = '/dev/ttyACM0'  # Change this to the appropriate port on your system
    baudrate = 9600

    for nmea_message in read_nmea_messages(port, baudrate):
        print(nmea_message)

if __name__ == '__main__':
    main()




# import serial

# # Set the USB port and baud rate
# port = '/dev/ttyUSB0'
# baud_rate = 57600

# # Open the serial connection
# ser = serial.Serial(port, baud_rate)

# # Continuously read and print data from the USB port
# while True:
#     data = ser.readline()
#     print(data)
