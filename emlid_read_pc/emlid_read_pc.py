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
