#include <Time.h>
#include <pb.h>
#include <pb_encode.h>
#include <adcvalues.pb.h>

unsigned short sensorValue0;
unsigned long runtime;
unsigned int unixtime;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while(!Serial){
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  sensorValue0 = analogRead(A0);
  runtime = millis();
  unixtime = now();
  
  SerialData message = {runtime, unixtime, sensorValue0};
  
  uint8_t buffer[16];
  pb_ostream_t stream = pb_ostream_from_buffer(buffer, sizeof(buffer));
  pb_encode(&stream, SerialData_fields, &message);
  for(int i=0; i < stream.bytes_written; i++){
    Serial.write(buffer[i]);
  }
  Serial.write("\n");
 }
