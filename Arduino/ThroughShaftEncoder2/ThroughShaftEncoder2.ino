#include <SoftwareSerial.h>

//SoftwareSerial mySerial(2, 3); // RX, TX

const int EncoderSignal = A0;
const int maxAnalog = 1023;
const int BAUD_RATE = 9600;

const int numReadings = 200;
const int timeBtwnReadings = 1;

double currReading = 0;
double lastReading = 0;
double currAngle = 0.0;
double delta = 0;

boolean start_bit = 0;
boolean stop_bit = 1;
boolean read_bit = 0;
byte command = 'a';

int angleTolerance = 60;

double encoderData[numReadings];
int timeData[numReadings];
unsigned long startTime = 0;
int index=0;

void setup() {
  pinMode(EncoderSignal, INPUT);
  //mySerial.begin(BAUD_RATE); //UNCOMMENT ME!!!
  Serial.begin(BAUD_RATE);
  while (!Serial) {
    ;
  }
}

void loop(){
  if (Serial.available()){
    command = Serial.read();
    //Serial.println("Receiving command");
    if (command == 'g'){
      //Serial.println("Received g");
      start_bit = 1;
      stop_bit = 0;
      command = 'a';
      initAngle();
      }
    else if (command == 's'){
      //Serial.println("Received s");
      start_bit = 0;
      stop_bit = 1;
      command = 'a';
      }
    else if (command == 'r'){
      //Serial.println("Received r");
      start_bit = 0;
      stop_bit = 1;
      read_bit = 1;
      command = 'a';
      }
    }
  else if (start_bit == 1 && stop_bit == 0 && index<numReadings){
    encoderLoop();
    }
  else if (read_bit == 1){
    toJetson();
    read_bit = 0;
    }
  }

void encoderLoop() {  
  currReading = GetAngle();
  delta = currReading - lastReading;

  if (delta < -angleTolerance) {
    delta = delta + 360;
    }
  /*else if (delta > angleTolerance) {
    delta = delta - 360;
    }*/ //With current config, number should always be increasing.

  currAngle += delta;

  //Serial.write('a');
  //Serial.println(currAngle);
  //Serial.println('d',currAngle);
  lastReading = currReading;

  if ((currAngle - encoderData[index-1])>0.5 && timeData[index-1]+timeBtwnReadings <= (int)millis()-startTime){
    encoderData[index] = currAngle;
    timeData[index] = (int)(millis() - startTime);
    index++;
    }

  /*else if ((currAngle - encoderData[index-1]) && timeData[index-1] <= (int)millis() && index<150){
    encoderData[index] = currAngle;
    timeData[index] = millis();
    index++;
    }*/

}

double GetAngle(){
  return (double)analogRead(EncoderSignal) / maxAnalog * 360;
}

void toJetson(){
  //Serial.println("To Jetson");
  for(int i=0; i<numReadings; i++){
    if (Serial.availableForWrite()){
      Serial.print(timeData[i] - startTime); 
      Serial.print(", ");
      Serial.println(encoderData[i]);
      timeData[i] = 0;
      encoderData[i] = 0;
      }
    else {
      i--;
      }
    }
  index = 0;
}

int initAngle(){
  delta = 100;
  lastReading = GetAngle();
  delay(0.5);
  while (delta > 1 || delta < -1){
    currReading = GetAngle();
    delta = currReading - lastReading;
    lastReading = currReading;
    }
  Serial.println("Last Reading: ");
  Serial.println(lastReading);
  Serial.println("");
  currAngle = 0;
  startTime = millis();

  timeData[0] = 0;
  encoderData[0] = 0;
  index = 1;
  
  return currReading;
}

double toRadians(int angle){
  return (double)angle / numReadings * 3.141592;
  }
