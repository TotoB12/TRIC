# [all_plot.py](https://github.com/TotoB12/TRIC/blob/main/all_plot/all_plot.py) Script Documentation

The [all_plot.py](https://github.com/TotoB12/TRIC/blob/main/all_plot/all_plot.py) script is the main script of the repository that combines all the data, processes it, and generates 2D and 3D visualizations using the Plotly library. This script gathers data from GPS and distance sensor arrays, processes and stores the data, and then generates interactive visualizations of the data points over time.

## Table of Contents

- [Functionality](#functionality)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Inputs](#inputs)
    - [GPS Serial Port](#gps-serial-port)
    - [Arduino Serial Port](#arduino-serial-port)
  - [Outputs](#outputs)
    - [3D Map Visualization](#3d-map-visualization)
    - [2D Graph Visualization](#2d-graph-visualization)

---

## Functionality

The "all_plot.py" script performs the following tasks:

1. Establishes serial connections to both a GPS module (Emlid Reach ...) and an Arduino board with distance sensors.
2. Reads data from the GPS module and distance sensors in real-time.
3. Parses GPS data (ZDA, GGA, RMC NMEA sentences) to extract timestamp, latitude, longitude, and direction information.
4. Parses distance sensor data from the Arduino to obtain distances from each of the seven sensors.
5. Calculates relative x and y coordinates based on UTM conversions from GPS latitude and longitude.
6. Records the parsed data into a file, separating the data by timestamp, coordinates, direction, and distances.
7. Processes the recorded data to smooth out the distance values using a moving average algorithm.
8. Generates 3D map visualizations that display the movement of sensor arrays over time using Plotly's 3D Scatter Plot.
9. Generates 2D graph visualizations of distance values over time using Plotly's 2D Line Plot.
10. Saves the generated visualizations as HTML files.

## Inputs and Outputs

### Inputs

#### GPS Serial Port

- **Description:** The script establishes a serial connection to the Emlid Reach GPS module via the specified serial port (`COM9` in this script).
- **Type:** Serial Port
- **Communication Settings:** Baud rate: 11520.

#### Arduino Serial Port

- **Description:** The script establishes a serial connection to the Arduino board with distance sensors via the specified serial port (`COM7` in this script).
- **Type:** Serial Port
- **Communication Settings:** Baud rate: 9600.

### Outputs

#### 3D Map Visualization

- **Description:** The script generates an interactive 3D map visualization of the sensor arrays' movement over time using Plotly's 3D Scatter Plot.
- **Output Format:** The visualization displays multiple colored markers representing each sensor array's position. The colors of the markers are scaled based on the corresponding distance values, and the Z-axis represents the distance from the ground.
- **Example:** [3D_Map.html](https://github.com/TotoB12/TRIC/edit/main/map_examples/map7.html) (just an example: only one mapped line)

#### 2D Graph Visualization

- **Description:** The script generates interactive 2D graph visualizations of distance values over time using Plotly's 2D Line Plot.
- **Output Format:** The visualization shows how the distance values from each sensor array change over time. The X-axis represents time, and the Y-axis represents the distance values. The colors of the lines are scaled based on the corresponding distance values.
- **Example:** [2D_Graph.html](https://github.com/TotoB12/TRIC/edit/main/graph_examples/graph.html) (just an example: only one graphed line)

---

**Note:** The script requires proper serial communication setup for both the GPS module and the Arduino board. The specified serial ports (`COM9` and `COM7`) need to be accurate. The script also requires the Plotly library for generating visualizations.
