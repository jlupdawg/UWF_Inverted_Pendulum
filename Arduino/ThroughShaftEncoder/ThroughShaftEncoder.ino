
#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX

const int EncoderSignal = A0;
const int upperMargin = 900;
const int maxAnalog = 1023;

int currReading = 0;
int lastReading = 0;
int currAngle = 0;
int diffReading = 0;




void setup() {
  pinMode(EncoderSignal, INPUT);
  mySerial.begin(115200); //UNCOMMENT ME!!!
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Native USB only
  }
}

void loop() {
  currReading = GetAngle();
  

  if(currReading > upperMargin){
    diffReading =  (lastReading+maxAnalog) - currReading;
  }
  
  toJetson(currAngle);
  lastReading = currReading;
}

int GetAngle(){
  return analogRead(EncoderSignal);
}

void toJetson(int angle){
    if (mySerial.available())
      Serial.write(angle);
}
