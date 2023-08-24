# [arduino_script.ino](https://github.com/TotoB12/TRIC/blob/main/arduino_script/arduino_script.ino) Documentation

The [arduino_script.ino](https://github.com/TotoB12/TRIC/blob/main/arduino_script/arduino_script.ino) is an Arduino sketch designed to interface with multiple ultrasonic distance sensors and measure distances using the time-of-flight principle. The script reads distances from seven ultrasonic sensors and outputs the measured distances to the Serial Monitor.

## Table of Contents

- [Functionality](#functionality)
- [Pin Configuration](#pin-configuration)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Inputs](#inputs)
    - [Ultrasonic Sensors](#ultrasonic-sensors)
  - [Outputs](#outputs)
    - [Serial Monitor Output](#serial-monitor-output)

---

## Functionality

The script utilizes multiple ultrasonic distance sensors to measure distances to obstacles in their line of sight. It employs the time-of-flight principle, where the time taken for a sound pulse to travel to the obstacle and back is used to calculate the distance. The distances measured by the sensors are then output to the Serial Monitor.

## Pin Configuration

The script assigns pins for trigger (trig) and echo (echo) connections for each of the seven ultrasonic sensors. These pins are used for both sending the trigger signal and receiving the echo signal.

- `trigPin1` to `trigPin7`: Trigger pins for the seven sensors.
- `echoPin1` to `echoPin7`: Echo pins for the seven sensors.

## Inputs and Outputs

### Inputs

#### Ultrasonic Sensors

- **Description:** The script interfaces with seven ultrasonic distance sensors. It sends trigger signals to these sensors and reads the echo signals to measure distances.
- **Type:** Physical Inputs (Ultrasonic Sensors)
- **Communication:** The script sends a brief pulse on the trigger pin to initiate a distance measurement. It then listens for the return echo pulse and measures the time it takes for the pulse to return.

### Outputs

#### Serial Monitor Output

- **Description:** The measured distances from the seven ultrasonic sensors are printed to the Serial Monitor. The distances are output as comma-separated values in centimeters.
- **Output Format:** The measured distances from each sensor are displayed sequentially as a single line of comma-separated values, e.g., `23, 50, 75, 100, 120, 150, 180`.

---

**Note:** Ensure the sensors are correctly connected to the specified trigger and echo pins.
