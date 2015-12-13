#include <pb.h>
#include <pb_encode.h>
#include <adcvalues.pb.h>

unsigned int adc0;
unsigned int adc1;
unsigned int adc2;
unsigned int adc3;
unsigned long runtime;


  
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while(!Serial){
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  adc0 = analogRead(A0);
  adc1 = analogRead(A1);
  adc2 = analogRead(A2);
  adc3 = analogRead(A3);
  runtime = millis();
  
  SerialData message = {runtime, adc0, adc1, adc2, adc3};
  uint8_t buffer[32];
  pb_ostream_t stream = pb_ostream_from_buffer(buffer, sizeof(buffer));
  pb_encode(&stream, SerialData_fields, &message);
  for(int i=0; i < stream.bytes_written; i++){
    Serial.write(buffer[i]);
  }
  Serial.write("\n");
 }

