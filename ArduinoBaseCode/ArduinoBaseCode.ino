/*  Honeywell 600EN-128-CBL
  Red, 5V
  Orange, D20 (Must be a hardware interrupt pin)
  Yellow, D21 (Must be a hardware interrupt pin)
  Green, Ground
*/

/*Motor Controller Shield

*/

/* Functions
   checkEnc() //retrieves angle and tick
   forward(duty cycle, delay in ms) //foward at DC
   backward(duty cycle, delay in ms) //backward at DC
   Stop() //stops the motors
   loggingData() //serial prints values
*/

#include <Encoder.h>

Encoder myEnc(20, 21);

#define rightPWM 9
#define rightDirection 7
#define leftPWM 10
#define leftDirection 8
#define goPin 22


const int derivativeDelay = 20000; //delay in derivative in microscends

float P = 1.0; //P gain
float D = 1.0; //D gain

const int deadZone = 1; //+-angle where action will not occur
const int highAngle = 60; //+- angle of no return
const int measurements = 2; //measurements to perform derivative
const float minDC = .2; //minimum duty cycle
const float maxDC = 1; //max duty cycle
const int maxMotorPWM = 255;

long oldPosition = 0;
int angle[measurements];
long newPosition = 0;
float d = 0;

unsigned long currentTime = 0;
unsigned long lastTime = 0;
float PD = 0;

bool Stat = false;

void setup() {
  pinMode(rightPWM, OUTPUT);
  pinMode(rightDirection, OUTPUT);
  pinMode(leftPWM, OUTPUT);
  pinMode(leftDirection, OUTPUT);
  pinMode(goPin, INPUT_PULLUP);

  Serial.begin(9600);
}




void loop() {
  P = (float) 1 / (highAngle - deadZone);
  D = 0;
  
  while (Stat)
  {
    derivative(derivativeDelay); //Delay in microseconds
    PD = abs(P * angle[measurements-1] + D * d);
    PD = max(PD, minDC);
    PD = min(PD, maxDC);

    if (angle[measurements-1] > deadZone)
    {
      backward(PD);
      Serial.print("Backward at "); Serial.print(PD * 100); Serial.println("%");

    }
    else if (angle[measurements-1] < -deadZone)
    {
      forward(PD);
      Serial.print("Forward at "); Serial.print(PD * 100); Serial.println("%");
    }
    else
    {
      Stop();
      Serial.println("STOP");
    }

    loggingData();
    Stat = !digitalRead(goPin);
    delay(100);
  }
  Stat = !digitalRead(goPin);
}


void loggingData()
{
  Serial.print("Tick : "); Serial.println(newPosition);
  Serial.print("Angle : "); Serial.println(angle[measurements-1]);
  Serial.print("d : "); Serial.println(d, 4);
}


