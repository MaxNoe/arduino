void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while(!Serial){
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned int sensorValue0 = analogRead(A0);
  unsigned long t = millis();
  
  Serial.print("{\"t\":");  
  Serial.print(t);
  Serial.print(", \"adc\":");
  Serial.print(sensorValue0);
  Serial.println("}");
}
