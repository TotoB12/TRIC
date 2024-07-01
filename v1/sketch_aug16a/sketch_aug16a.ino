 
int trigPin1 = A2;    // Trigger
int echoPin1 = A1;    // Echo  
long duration1, cm1;
 
void setup() {
  Serial.begin (9600);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
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
  Serial.println();
  
  delay(1000);
}