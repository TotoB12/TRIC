# TRIC

## Files
ultrasonic_sensor.ino prints out live the time taken for the ultrasonic sensor to capture back it's signal. This script allows us to calculate the speed of sound in the current temperature.

telemetre.ino print out the live distance captured by the ultrasonic sensor, using the speed of sound determined with the help of ultrasonic_sensor.ino.

gps.ino reads GPS data using TinyGPS++, and displays the latitude and longitude. It also measures distance using the ultrasonic sensor and print it out as well.

emlid_read_pc.py streams the raw NMEA data from a USB connected REACH module to a Windows terminal, and parses it to make readable.

arduino_read_pc.py streams the raw ultrasonic data from a USB connected arduino to a Windows terminal.

get_all.py combines the data from both the Arduino and the Emlid into one stream.

## Info
### Desk Coordinates:

34.91115 N, 120.44627 W

Connected a REACH RS+ as a base to a REACH M2 by LoRa by 902.0 MHz at 18.23 kb/s.

### Temperature impact on speed of sound
| Celsius temperature θ (°C) | Speed of sound c (m/s) |
|----------------------------|------------------------|
| 35                         | 351.88                 |
| 30                         | 351.88                 |
| 25                         | 346.13                 |
| 20                         | 343.21                 |
| 15                         | 340.27                 |
| 10                         | 337.31                 |
| 5                          | 334.32                 |
| 0                          | 331.30                 |
| -5                         | 328.25                 |
| -10                        | 325.18                 |
| -15                        | 322.07                 |
| -20                        | 318.94                 |
| -25                        | 315.77                 |

## Links

[https://community.emlid.com/t/emlid-reach-to-arduino-uno/6230](https://community.emlid.com/t/emlid-reach-to-arduino-uno/6230) <br>
[https://community.emlid.com/t/python-usb-to-pc/27022/4](https://community.emlid.com/t/python-usb-to-pc/27022/4) <br>
[https://forums.raspberrypi.com//viewtopic.php?t=106468](https://forums.raspberrypi.com//viewtopic.php?t=106468)
