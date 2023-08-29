# [arduino_read_pc.py](https://github.com/TotoB12/TRIC/blob/main/arduino_read_pc/arduino_read_pc.py) Script Documentation

The [arduino_read_pc.py](https://github.com/TotoB12/TRIC/blob/main/arduino_read_pc/arduino_read_pc.py) script is a Python program designed to read data from an Arduino board connected to a computer via a serial port. It reads and displays data sent by the Arduino over the serial connection in real-time.

## Table of Contents

- [Functionality](#functionality)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Inputs](#inputs)
    - [Serial Port](#serial-port)
  - [Outputs](#outputs)
    - [Arduino Data](#arduino-data)

---

## Functionality

The script establishes a serial connection to an Arduino board connected to the specified serial port (`COM3` in this script) and reads the data being sent by the Arduino. It continuously listens for incoming data and displays it in the terminal window.

## Inputs and Outputs

### Inputs

#### Serial Port

- **Description:** The script establishes a serial connection to the Arduino board via the specified serial port (`COM3` in this script).
- **Type:** Serial Port
- **Communication Settings:** Baud rate: 9600.

### Outputs

#### Arduino Data

- **Description:** The script reads data being sent by the Arduino over the serial connection and displays it in the terminal window.
- **Output Format:** The script reads each line of data sent by the Arduino and displays it as text in the terminal. It reads and prints the data in real-time as it is received from the Arduino.

---

**Note:** The script assumes that the Arduino is sending data over the serial connection and that the data is encoded in ASCII format, preferably using [arduino_script.ino](https://github.com/TotoB12/TRIC/blob/main/arduino_script/arduino_script.ino).
