#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX

const int EncoderSignal = A0;
const int maxAnalog = 1023;
const int BAUD_RATE = 9600;

double currReading = 0;
double lastReading = 0;
double currAngle = 0.0;
double delta = 0;

int angleTolerance = 30;

void setup() {
  pinMode(EncoderSignal, INPUT);
  //mySerial.begin(BAUD_RATE); //UNCOMMENT ME!!!
  Serial.begin(BAUD_RATE);
  while (!Serial) {
    ;
  }
  initAngle();
}

void loop() {
  currReading = GetAngle();
  delta = currReading - lastReading;

  if (delta < -angleTolerance) {
    delta = delta + 360;
    }
  else if (delta > angleTolerance) {
    delta = delta - 360;
    }

  currAngle += delta;  
  toJetson(currAngle);
  
  Serial.println(currAngle);
  lastReading = currReading;
}

double GetAngle(){
  return (double)analogRead(EncoderSignal) / maxAnalog * 360;
}

void toJetson(int angle){
    if (mySerial.available())
      Serial.write(angle);
}

int initAngle(){
  delta = 100;
  lastReading = GetAngle();
  delay(1);
  while (delta > 1 || delta < -1){
    currReading = GetAngle();
    delta = currReading - lastReading;
    lastReading = currReading;
    }
  return currReading;
}

double toRadians(int angle){
  return (double)angle / 180 * 3.141592;
  }
