# [generate_data.py](https://github.com/TotoB12/TRIC/blob/main/v1/generate_data/generate_data.py) Script Documentation

The [generate_data.py](https://github.com/TotoB12/TRIC/blob/main/v1/generate_data/generate_data.py) script generates sample data that can be used as input for the [file_plot.py](https://github.com/TotoB12/TRIC/blob/main/v1/file_plot/file_plot.py) script. This script creates a text file containing simulated timestamped coordinates and a corresponding z-axis value.

## Table of Contents

- [Functionality](#functionality)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Inputs](#inputs)
    - [Number of Lines](#number-of-lines)
  - [Outputs](#outputs)
    - [Generated Data File](#generated-data-file)

---

## Functionality

The script simulates the generation of data points over time. It creates a text file named `data.txt` in a subdirectory named `data`. The generated data includes timestamps, X and Y coordinate displacements, and a z-axis value for each data point. The X and Y coordinate displacements are randomly generated values within a specified range, and the z-axis value is a random integer between 35 and 40.

## Inputs and Outputs

### Inputs

#### Number of Lines

- **Description:** The user is prompted to input the number of lines (data points) to generate for the data file.
- **Type:** User Input (Integer)
- **Usage:** The number of lines determines the amount of sample data to generate.

### Outputs

#### Generated Data File

- **Description:** The script generates a text file named `data.txt` in a subdirectory named `data`. Each line in the file represents a data point with the following format:
  ```
  timestamp, x_position, y_position, z_value
  ```
- **Format:**
  - `timestamp`: Timestamp in the format "YYYY-MM-DD_HH:MM:SS.sss", representing the time when the data point was generated.
  - `x_position`: Randomly generated X coordinate position value within the range of -0.02 to 0.02.
  - `y_position`: Randomly generated Y coordinate position value within the range of -0.02 to 0.02.
  - `z_value`: Randomly generated integer value between 35 and 40, representing the z-axis value.

---

**Note:** The script is intended to generate sample data for testing and visualization purposes. The generated data can be used as input for the [file_plot.py](https://github.com/TotoB12/TRIC/blob/main/file_plot/file_plot.py) script, which plots the data points over time.
