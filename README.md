# TRIC

## Files
ultrasonic_sensor.ino prints out live the time taken for the ultrasonic sensor to capture back it's signal. This script allows us to calculate the speed of sound in the current temperature.

telemetre.ino print out the live distance captured by the ultrasonic sensor, using the speed of sound determined with the help of ultrasonic_sensor.ino.

gps.ino reads GPS data using TinyGPS++, and displays the latitude and longitude. It also measures distance using the ultrasonic sensor and print it out as well.

## Info
DESK COORD:

34.91115 N, 120.44627 W

Connected a REACH RS+ as a base to a REACH M2 by LoRa at 902.0 MHz at 18.23 kb/s.

## Links

[https://community.emlid.com/t/emlid-reach-to-arduino-uno/6230](https://community.emlid.com/t/emlid-reach-to-arduino-uno/6230)
