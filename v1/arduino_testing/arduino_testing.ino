#define sensorPin A0

int distance = 0;

void setup() {
  Serial.begin(9600);
}

void read_sensor() {
  distance = analogRead(sensorPin) * 1;
}

void print_data() {
  Serial.print(distance);
  Serial.print('\n');
}

void loop() {
  read_sensor();
  print_data();
  delay(1000);
}