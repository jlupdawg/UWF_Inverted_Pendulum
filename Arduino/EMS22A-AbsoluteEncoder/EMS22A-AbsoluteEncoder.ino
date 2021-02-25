/* Encoder Pinout:
 * 1 - Digital In (Grounded for single sensor) - GND
 * 2 - Clock - 6
 * 3 - GND
 * 4 - Digital Output - 7
 * 5 - VCC
 * 6 - CS - 5
 * 
 * Use AtMega328P Old Bootloader
 */

const int PIN_CS = 5;
const int PIN_CLOCK = 6;
const int PIN_DATA = 7;
const int ZERO_SET = 333;
const int MAX_ENC = 1020;

char cmd = 'x';
int pos = 0;
float offset = 0;
    
void setup() {
  Serial.begin(115200);
  pinMode(PIN_CS, OUTPUT);
  pinMode(PIN_CLOCK, OUTPUT);
  pinMode(PIN_DATA, INPUT);

  digitalWrite(PIN_CLOCK, HIGH);
  digitalWrite(PIN_CS, LOW);
}


//byte stream[16];
void loop() {
    if (Serial.available()){
    cmd = Serial.read();
    //Serial.println(cmd);
    }

    if(cmd == 'r'){
      //Serial.print("The angle is: ");
      Serial.println(GetAngle(pos));
      cmd = 'x';
    }
    else if(cmd == 's'){
      offset = 0;
      offset = GetAngle(pos);
      //Serial.println(offset);
      cmd = 'x';
    }
  
    digitalWrite(PIN_CS, HIGH);
    delay(1);
    digitalWrite(PIN_CS, LOW);
    pos = 0;
    for (int i=0; i<10; i++) {
      digitalWrite(PIN_CLOCK, LOW);
      digitalWrite(PIN_CLOCK, HIGH);
     
      byte b = digitalRead(PIN_DATA) == HIGH ? 1 : 0;
      pos += b * pow(2, 10-(i+1));
    }
    for (int i=0; i<6; i++) {
      digitalWrite(PIN_CLOCK, LOW);
      digitalWrite(PIN_CLOCK, HIGH);
    }
    digitalWrite(PIN_CLOCK, LOW);
    digitalWrite(PIN_CLOCK, HIGH);
    //Serial.print("POSITION: "); Serial.print(pos); Serial.print(" : "); Serial.print("ANGLE: "); Serial.println(GetAngle(pos));
    

}

int GetAngle(int pos){
  int angle = 0;
  if(pos < ZERO_SET){
    pos = MAX_ENC - ZERO_SET + pos;
  }
  else{
    pos = pos - ZERO_SET;
  }

  angle = map(pos, 0, 1020, 0, 360);
  //Serial.print("ADJUSTED POSITION: "); Serial.println(pos);
  if(angle > 180){
    angle = angle-360;
  }
  //Serial.print("Inside the fxn, the offset is: ");
  //Serial.println(offset);
  return (angle - offset);
}
