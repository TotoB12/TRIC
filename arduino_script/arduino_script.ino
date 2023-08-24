int trigPin1 = A2;    // Trigger
int echoPin1 = A1;    // Echo 
int trigPin2 = 7;    // Trigger
int echoPin2 = 6;    // Echo 
int trigPin3 = 9;    // Trigger
int echoPin3 = 8;    // Echo 
int trigPin4 = 3;    // Trigger
int echoPin4 = 2;    // Echo 
int trigPin5 = A0;    // Trigger
int echoPin5 = 12;    // Echo 
int trigPin6 = 5;    // Trigger
int echoPin6 = 4;    // Echo 
int trigPin7 = 11;    // Trigger
int echoPin7 = 10;    // Echo
long duration1, cm1, duration2, cm2, duration3, cm3, duration4, cm4, duration5, cm5, duration6, cm6, duration7, cm7;
 
void setup() {
  Serial.begin (9600);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin3, INPUT);
  pinMode(trigPin4, OUTPUT);
  pinMode(echoPin4, INPUT);
  pinMode(trigPin5, OUTPUT);
  pinMode(echoPin5, INPUT);
  pinMode(trigPin6, OUTPUT);
  pinMode(echoPin6, INPUT);
  pinMode(trigPin7, OUTPUT);
  pinMode(echoPin7, INPUT);
}
 
void loop() {
  for (int i = 0; i < 7; i++) {
    int currentTrigPin, currentEchoPin;
    long *currentDuration, *currentCm;

    // Assign the current trig and echo pins, duration, and cm variables
    switch (i) {
      case 0:
        currentTrigPin = trigPin1;
        currentEchoPin = echoPin1;
        currentDuration = &duration1;
        currentCm = &cm1;
        break;
      case 1:
        currentTrigPin = trigPin2;
        currentEchoPin = echoPin2;
        currentDuration = &duration2;
        currentCm = &cm2;
        break;
      case 2:
        currentTrigPin = trigPin3;
        currentEchoPin = echoPin3;
        currentDuration = &duration3;
        currentCm = &cm3;
        break;
      case 3:
        currentTrigPin = trigPin4;
        currentEchoPin = echoPin4;
        currentDuration = &duration4;
        currentCm = &cm4;
        break;
      case 4:
        currentTrigPin = trigPin5;
        currentEchoPin = echoPin5;
        currentDuration = &duration5;
        currentCm = &cm5;
        break;
      case 5:
        currentTrigPin = trigPin6;
        currentEchoPin = echoPin6;
        currentDuration = &duration6;
        currentCm = &cm6;
        break;
      case 6:
        currentTrigPin = trigPin7;
        currentEchoPin = echoPin7;
        currentDuration = &duration7;
        currentCm = &cm7;
        break;
    }

    // Trigger the current sensor
    digitalWrite(currentTrigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(currentTrigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(currentTrigPin, LOW);

    // Read the signal from the current sensor
    pinMode(currentEchoPin, INPUT);
    *currentDuration = pulseIn(currentEchoPin, HIGH);

    *currentCm = (*currentDuration / 2) / 29.1;

    delay(10);
  }

  Serial.print(cm1);
  Serial.print(", ");
  Serial.print(cm2);
  Serial.print(", ");
  Serial.print(cm3);
  Serial.print(", ");
  Serial.print(cm4);
  Serial.print(", ");
  Serial.print(cm5);
  Serial.print(", ");
  Serial.print(cm6);
  Serial.print(", ");
  Serial.print(cm7);
  Serial.println();
  
  delay(1000);
}