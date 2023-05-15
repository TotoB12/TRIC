#include <TinyGPS++.h>
#include <SoftwareSerial.h>
/*
   This sample code demonstrates the normal use of a TinyGPS++ (TinyGPSPlus) object.
   It requires the use of SoftwareSerial, and assumes that you have a
   4800-baud serial GPS device hooked up on pins 4(rx) and 3(tx).
   
LC20031 pinout(Top View *pins down*  L to R 5 to 1 
  GND-5
  GND-4
  TX-3
  RX-2
  3.3V-1


Emlid Reach 
Power Reach Via the USB cable 
White-GPS RX
Blue GPS TX
 
*/
// The TinyGPS++ object
TinyGPSPlus gps;
int i=0;
// The serial connection to the GPS device 
SoftwareSerial ss(3, 4);// GPSTX to 4, GPSRX  to 3  // this part go switched around and may be the issue k

void setup()
{
  Serial.begin(9600);
  ss.begin(57600);//GPS Baud Rate

  Serial.println(F("GPS SatsLatLong"));
  Serial.println(F("Outputs Latitude and longitude"));
  Serial.println(F("Jake Falck"));
  Serial.println();
  

}

void loop()
{
  while (Serial.available() < 1) {} // Wait until a character is received
char val = Serial.read();
Serial.flush();
if (val == 'g'){
   Serial.println(F("Sats Latitude   Longitude"));
  Serial.println(F("     (deg)      (deg)    "));
  Serial.println(F("-------------------------"));
  printInt(gps.satellites.value(), gps.satellites.isValid(), 5);
  printFloat(gps.location.lat(), gps.location.isValid(), 11, 6);
  printFloat(gps.location.lng(), gps.location.isValid(), 12, 6);
  Serial.println();
  Serial.println();
  i++;

}
  if (millis() > 5000 && gps.charsProcessed() < 10)
    Serial.println(F("Error: GPS data received(check wiring)"));
}

// This custom version of delay() ensures that the gps object
// is being "fed".
static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (ss.available())
      gps.encode(ss.read());
  } while (millis() - start < ms);
}

static void printFloat(float val, bool valid, int len, int prec)
{
  if (!valid)
  {
    while (len-- > 1)
      Serial.print('*');
    Serial.print(' ');
  }
  else
  {
    Serial.print(val, prec);
    int vi = abs((int)val);
    int flen = prec + (val < 0.0 ? 2 : 1); // . and -
    flen += vi >= 1000 ? 4 : vi >= 100 ? 3 : vi >= 10 ? 2 : 1;
    for (int i=flen; i<len; ++i)
      Serial.print(' ');
  }
  smartDelay(0);
}

static void printInt(unsigned long val, bool valid, int len)
{
  char sz[32] = "*****************";
  if (valid)
    sprintf(sz, "%ld", val);
  sz[len] = 0;
  for (int i=strlen(sz); i<len; ++i)
    sz[i] = ' ';
  if (len > 0) 
    sz[len-1] = ' ';
  Serial.print(sz);
  smartDelay(0);
}

static void printDateTime(TinyGPSDate &d, TinyGPSTime &t)
{
  if (!d.isValid())
  {
    Serial.print(F("********** "));
  }
  else
  {
    char sz[32];
    sprintf(sz, "%02d/%02d/%02d ", d.month(), d.day(), d.year());
    Serial.print(sz);
  }
  
  if (!t.isValid())
  {
    Serial.print(F("******** "));
  }
  else
  {
    char sz[32];
    sprintf(sz, "%02d:%02d:%02d ", t.hour(), t.minute(), t.second());
    Serial.print(sz);
  }

  printInt(d.age(), d.isValid(), 5);
  smartDelay(0);
}

static void printStr(const char *str, int len)
{
  int slen = strlen(str);
  for (int i=0; i<len; ++i)
    Serial.print(i<slen ? str[i] : ' ');
  smartDelay(0);
}
