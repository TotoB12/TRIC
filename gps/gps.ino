#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>

const int GPS_RX = 9;
const int GPS_TX = 10;
SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
TinyGPSPlus gps;

void setup() {
  pinMode(pinTrig, OUTPUT);
  pinMode(pinEcho, INPUT);
  digitalWrite(pinTrig, LOW);
  Serial.begin(9600);
  gpsSerial.begin(9600); // setup gps
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("distance");
  lcd.setCursor(8, 1);
  lcd.print("cm");
}

void loop() {
  // read GPS
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  // display info
  if (gps.location.isValid()) {
    Serial.print("Latitude: ");
    Serial.println(gps.location.lat(), 6);
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);
  } else {
    Serial.println("No GPS fix");
  }

  // from telemetre.ino
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);
  Time = pulseIn(pinEcho, HIGH);
  if (Time > 25000) {
    Serial.println("mesure failure");
  } else {
    Distance = (344 * Time) / 20000;
    Serial.print("distance = ");
    Serial.print(Distance);
    Serial.println(" cm   ");
  }
  delay(5000);
  lcd.setCursor(0, 1);
  lcd.print(Distance);
}
