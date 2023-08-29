# [get_all.py](https://github.com/TotoB12/TRIC/blob/main/get_all/get_all.py) Script Documentation

The [get_all.py](https://github.com/TotoB12/TRIC/blob/main/get_all/get_all.py) script is a Python program designed to read and parse NMEA data from two different serial ports: one connected to an Emlid device and the other connected to an Arduino board with an ultrasonic distance sensor. The script combines the received data to provide location information from the GNSS? device along with distance measurements from the Arduino sensor. It also allows the user to stop the data collection using keyboard shortcuts.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Function](#function)
  - [`parse_nmea_data(data)`](#`parse_nmea(data)`-function)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Inputs](#inputs)
    - [Emlid Serial Port](#emlid-serial-port)
    - [Arduino Serial Port](#arduino-serial-port)
    - [Keyboard Input](#keyboard-input)
  - [Outputs](#outputs)
    - [Parsed Data](#parsed-data)

---

## Prerequisites

- Emlid GNSS device connected to a serial port (`COM4` in this script) with NMEA data output.
- Arduino board connected to a serial port (`COM3` in this script) with distance sensor data output.

## Function

### `parse_nmea_data(data)` Function

- **Description:** This function parses NMEA data strings to extract relevant information, specifically when the NMEA data is of the GNGGA type. It processes the latitude, longitude, and time data from the parsed NMEA sentence.
- **Input:**
  - `data` (string): NMEA data string to be parsed.
- **Output:**
  - Parsed data string containing time, latitude, and longitude information.

## Inputs and Outputs

### Inputs

#### Emlid Serial Port

- **Description:** This script connects to an Emlid device via a specified serial port (`COM4` in this script) to read NMEA data.
- **Type:** Serial Port
- **Communication Settings:** Baud rate: 57600, Timeout: 0.1 seconds.

#### Arduino Serial Port

- **Description:** This script connects to an Arduino board with an ultrasonic distance sensor via a specified serial port (`COM3` in this script) to read distance measurements.
- **Type:** Serial Port
- **Communication Settings:** Baud rate: 9600, Timeout: 0.1 seconds.

#### Keyboard Input

- **Description:** The script monitors keyboard inputs using the `keyboard` library to allow the user to stop data collection by pressing the 's' or 'c' keys.
- **Type:** Keyboard Input
- **Actions:** Pressing 's' or 'c' keys stops the data collection and terminates the script.

### Outputs

#### Parsed Data

- **Description:** The script combines parsed data from the Emlid GNSS device (time, latitude, longitude) with distance measurements from the Arduino ultrasonic sensor. The combined data is printed to the console in the following format: `[Rover] Time: hh:mm:ss, Lat: dd°mm'ss.sss", Lon: ddd°mm'ss.sss", Dist: xx cm`.
