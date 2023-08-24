# emlid_plot.py Script Documentation

The "emlid_plot.py" script is a Python program designed to read and plot real-time geographic coordinates (latitude and longitude) from an Emlid GNSS device connected to a computer via a serial port. The script uses the Matplotlib library to visualize the movement of the device on a 2D plot. It converts latitude and longitude coordinates to UTM (Universal Transverse Mercator) coordinates to ensure accurate plotting.

## Table of Contents

- [Functionality](#functionality)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Inputs](#inputs)
    - [Serial Port](#serial-port)
  - [Outputs](#outputs)
    - [Real-Time Plot](#real-time-plot)

---

## Functionality

The script connects to an Emlid GNSS device via a specified serial port (`COM7` in this script) and reads NMEA data. It parses specific NMEA sentences of type "GNGGA" to extract time, latitude, and longitude information. The script then converts the latitude and longitude to UTM coordinates and plots the real-time movement of the device on a 2D plot.

## Inputs and Outputs

### Inputs

#### Serial Port

- **Description:** The script connects to the Emlid GNSS device via the specified serial port (`COM7` in this script).
- **Type:** Serial Port
- **Communication Settings:** Baud rate: 57600.

### Outputs

#### Real-Time Plot

- **Description:** The script plots the real-time movement of the device on a 2D plot. The plot is updated with each received NMEA sentence, showing the relative movement of the device from the initial point (the origin). The plot is displayed using the Matplotlib library.
- **Output Format:** The plotted points on the 2D plot represent the movement of the device in UTM coordinates. The script connects points using green circles, where each circle represents a device position. The initial point is used as the origin for plotting.

---

**Note:** Ensure the specified serial port (`COM7`) is accurate and that your Emlid GNSS device is properly connected to this port. The script assumes that the Emlid device is sending valid NMEA data over the serial connection.
