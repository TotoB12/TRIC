# [emlid_read_pc.py](https://github.com/TotoB12/TRIC/blob/main/v1/emlid_read_pc/emlid_read_pc.py) Script Documentation

The [emlid_read_pc.py](https://github.com/TotoB12/TRIC/blob/main/v1/emlid_read_pc/emlid_read_pc.py) script is a Python program designed to read and parse NMEA data from an Emlid GNSS device connected to a computer via a serial port. The script provides two modes: "Full" and "Clean." In the "Full" mode, it outputs raw NMEA data, while in the "Clean" mode, it parses and formats specific NMEA sentences for easier readability.

## Table of Contents

- [Functionality](#functionality)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Inputs](#inputs)
    - [User Input](#user-input)
  - [Outputs](#outputs)
    - [NMEA Data Output](#nmea-data-output)

---

## Functionality

The script connects to an Emlid GNSS device via a specified serial port (`COM4` in this script) and reads NMEA data. It offers two modes:

1. **Full Mode (`f`)**: Displays the raw NMEA data received from the device without any parsing or formatting.
2. **Clean Mode (`c`)**: Parses and formats specific NMEA sentences for easier interpretation. It extracts and displays relevant information, such as time, latitude, longitude, fix quality, number of satellites, and altitude.

## Inputs and Outputs

### Inputs

#### User Input

- **Description:** The user is prompted to choose between "Full" mode and "Clean" mode by entering either `f` or `c`.
- **Type:** User Input (String)
- **Usage:** The user's choice determines whether raw NMEA data or parsed and formatted data will be displayed.

### Outputs

#### NMEA Data Output

- **Description:** The script reads NMEA data from the Emlid GNSS device and outputs either raw data or parsed data based on the chosen mode.
- **Output Format:**
  - **Full Mode (`f`)**: Outputs the raw NMEA data received from the device without any modification.
  - **Clean Mode (`c`)**: Parses specific NMEA sentences of types "GNGGA" and "GNEBP" to extract relevant information. It outputs formatted data that includes time, latitude, longitude, fix quality, number of satellites, and altitude for "GNGGA" sentences, and base station information for "GNEBP" sentences.

---

**Note:** Ensure the specified serial port (`COM4`) is correct and that the Emlid device is properly connected to this port. The script assumes that the Emlid device is sending NMEA data over the serial connection.
