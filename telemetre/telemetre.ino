#include<LiquidCrystal.h>
LiquidCrystal lcd (12,11,5,4,3,2);
int pinTrig = 7;
int pinEcho = 6;
long Time;
float Distance;

void setup() {
pinMode(pinTrig,OUTPUT);
pinMode(pinEcho,INPUT);
digitalWrite(pinTrig,LOW);
Serial.begin(9600);
  lcd.begin(16,2);
  lcd.setCursor(0,0);
  lcd.print("distance");
  lcd.setCursor(8,1);
  lcd.print("cm");

}

void loop() {
digitalWrite(pinTrig,HIGH);
delayMicroseconds(10);
digitalWrite(pinTrig,LOW);
Temps = pulseIn(pinEcho,HIGH);
if(Temps > 25000){
  Serial.println("mesure failure");
}
else{
  Distance = (344*Time)/20000;
  Serial.print("distance = ");
  Serial.print(Distance);
  Serial.println(" cm   ");
  }
delay(5000);
lcd.setCursor(0,1);
lcd.print(Distance);

}
