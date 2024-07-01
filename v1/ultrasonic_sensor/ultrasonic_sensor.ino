int pinTrig = 3;
int pinEcho = 2;
long Time;

void setup() {
  pinMode(pinTrig,OUTPUT);
  pinMode(pinEcho,INPUT);
  digitalWrite(pinTrig,LOW);
  Serial.begin(9600);
}
void loop() {
  digitalWrite(pinTrig,HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig,LOW);
  Temps = pulseIn(pinEcho,HIGH);
  if (Temps>25000){
    Serial.println("mesure failure");
  }
else{
      Serial.print("time = ");
  Serial.print(Time);
  Serial.println(" microsecondes   ");
  }
delay(5000);
}
