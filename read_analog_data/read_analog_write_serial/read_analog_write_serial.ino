void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  int sensorValue0 = analogRead(A0);
  unsigned long t = millis();
  unsigned int voltage0 = sensorValue0;
    
  Serial.print(t);
  Serial.print(",");
  Serial.println(voltage0);
}
