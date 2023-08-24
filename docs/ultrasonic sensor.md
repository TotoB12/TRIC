# Ultrasonic Sensor Arduino Script Documentation

This Arduino script reads distance measurements from an ultrasonic distance sensor and communicates the results via the Serial Monitor. The script utilizes the HC-SR04 ultrasonic sensor, which emits ultrasonic pulses to measure distance based on the time it takes for the pulse to bounce back.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Loop](#loop)
- [Functions](#functions)
  - [`setup()`](#setup-function)
  - [`loop()`](#loop-function)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Inputs](#inputs)
    - [pinTrig](#pintrig)
    - [pinEcho](#pinecho)
  - [Outputs](#outputs)
    - [Serial Monitor Output](#serial-monitor-output)

---

## Prerequisites

- Arduino board.
- HC-SR04 ultrasonic distance sensor.
- Connection wires for wiring the sensor to the Arduino.

## Setup

The `setup()` function is called once when the Arduino starts. It performs the following tasks:

- Configures the `pinTrig` as an OUTPUT pin to send ultrasonic pulses.
- Configures the `pinEcho` as an INPUT pin to receive the echo signal.
- Initializes the Serial communication at a baud rate of 9600.

## Loop

The `loop()` function continuously executes the following steps:

1. Sends a short high pulse (10 microseconds) to the `pinTrig` to trigger the ultrasonic sensor.
2. Measures the time taken for the echo signal to return to the `pinEcho` using the `pulseIn()` function.
3. Checks if the measured time is greater than 25000 microseconds (25 milliseconds), which indicates a measurement failure.
4. If the measurement is successful, prints the measured time to the Serial Monitor.

## Functions

### `setup()` Function

The `setup()` function initializes the pins and Serial communication. It has no inputs or outputs.

### `loop()` Function

The `loop()` function is the main execution loop that performs distance measurements using the ultrasonic sensor. It has no inputs or outputs.

## Inputs and Outputs

### Inputs

#### `pinTrig`

- **Type:** Digital Output Pin
- **Description:** This pin is connected to the trigger (Trig) pin of the HC-SR04 sensor. It sends short pulses to initiate distance measurements.

#### `pinEcho`

- **Type:** Digital Input Pin
- **Description:** This pin is connected to the echo (Echo) pin of the HC-SR04 sensor. It receives the echo signal and measures the time it takes for the signal to return.

### Outputs

#### Serial Monitor Output

- **Type:** Serial Communication
- **Description:** The script communicates with the Serial Monitor at a baud rate of 9600. It outputs distance measurement results in microseconds. If the measured time exceeds 25000 microseconds, indicating a measurement failure, an appropriate message is displayed.

---

**Note:** For wiring connections and necessary libraries, refer to the [HC-SR04 datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) and Arduino reference documentation.
