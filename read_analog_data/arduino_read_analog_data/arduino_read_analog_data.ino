void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
}

void loop() {
  // put your main code here, to run repeatedly:
  int sensorValue0 = analogRead(A0);
  unsigned int t = millis();
  double voltage0 = sensorValue0*(5.0/1023.0);
    
  Serial.print(t);
  Serial.print(",");
  Serial.println(voltage0);
}
