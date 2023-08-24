# Telemetre Arduino Script Documentation

This Arduino script utilizes an ultrasonic distance sensor to measure distance and displays the results on an LCD screen. The script calculates the distance based on the time it takes for an ultrasonic pulse to bounce back and incorporates a LiquidCrystal library to display the measurements on a 16x2 character LCD.

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
    - [LCD Display](#lcd-display)

---

## Prerequisites

- Arduino board.
- HC-SR04 ultrasonic distance sensor.
- 16x2 character LCD with the LiquidCrystal library installed.
- Connection wires for wiring the sensor and LCD to the Arduino.

## Setup

The `setup()` function is called once when the Arduino starts. It performs the following tasks:

- Configures the `pinTrig` as an OUTPUT pin to send ultrasonic pulses.
- Configures the `pinEcho` as an INPUT pin to receive the echo signal.
- Initializes Serial communication at a baud rate of 9600.
- Initializes the LCD screen using the LiquidCrystal library and displays the initial messages on the screen.

## Loop

The `loop()` function continuously executes the following steps:

1. Sends a short high pulse (10 microseconds) to the `pinTrig` to trigger the ultrasonic sensor.
2. Measures the time taken for the echo signal to return to the `pinEcho` using the `pulseIn()` function.
3. Checks if the measured time is greater than 25000 microseconds (25 milliseconds), indicating a measurement failure.
4. If the measurement is successful, calculates the distance in centimeters using the speed of sound and the time taken.
5. Prints the calculated distance to the Serial Monitor and updates the LCD display with the new distance reading.

## Functions

### `setup()` Function

The `setup()` function initializes the pins, Serial communication, and LCD screen. It has no inputs or outputs.

### `loop()` Function

The `loop()` function is the main execution loop that performs distance measurements using the ultrasonic sensor and updates the LCD display. It has no inputs or outputs.

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
- **Description:** The script communicates with the Serial Monitor at a baud rate of 9600. It outputs distance measurement results in centimeters. If the measured time exceeds 25000 microseconds, indicating a measurement failure, an appropriate message is displayed.

#### LCD Display

- **Type:** Character LCD Display
- **Description:** The script uses the LiquidCrystal library to display distance measurements on a 16x2 character LCD. The LCD displays the text "distance" on the first line and the calculated distance in centimeters on the second line. The LCD display is updated in the `loop()` function.

---

**Note:** For wiring connections and necessary libraries, refer to the [HC-SR04 datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf), Arduino reference documentation
