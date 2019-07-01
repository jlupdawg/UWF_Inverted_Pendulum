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

float Kp = 1.0; //P gain
float Kd = 1.0; //D gain
float PD = 0;

const int deadZone = 1; //+-angle where action will not occur
const int highAngle = 20; //+- angle of no return
const int measurements = 5; //measurements to perform derivative
const float minDC = .25; //minimum duty cycle
const float maxDC = 1; //max duty cycle
const int maxMotorPWM = 255;
const int derivativeDelay = 8000;


long oldPosition = 0;
int angle[measurements];
long newPosition = 0;
float d = 0;
long dt = 0;

unsigned long currentTime = 0;
unsigned long lastTime = 0;

bool Stat = true;

void setup() {
  pinMode(rightPWM, OUTPUT);
  pinMode(rightDirection, OUTPUT);
  pinMode(leftPWM, OUTPUT);
  pinMode(leftDirection, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  Kp = .17;  //Kp .17
  Kd = .1;  //Kd .04

  while (Stat)
  {
    currentTime = millis();
    for (int i = 0; i < measurements; i++)
    {
      checkEnc();
      delayMicroseconds(derivativeDelay);
    }
    dt = (currentTime - lastTime) * 1000;
    derivative();
    lastTime = currentTime;
    Serial.print(angle[measurements - 1]); Serial.print(","); Serial.println(d);

    PD = abs(Kp * angle[measurements - 1] + Kd * d);

    PD = mapf(PD, 0, 1, minDC, maxDC);

    PD = max(PD, minDC);
    PD = min(PD, maxDC);
    Serial.println(PD);

    if (angle[measurements - 1] > deadZone)
    {
      forward(PD);
      Serial.print("Forward at "); Serial.print(PD*100); Serial.println("%");
    }
    else if (angle[measurements - 1] < -deadZone)
    {
      backward(PD);
      Serial.print("Backward at "); Serial.print(PD*100); Serial.println("%");
    }
    else
    {
      Stop();
      Serial.println("STOP");
    }

    loggingData();
    while (angle[measurements - 1] > highAngle || angle[measurements - 1] < -highAngle)
    {
      Stat = false;
      Serial.println("out of range");
      Stop();
    }
  }
  Stop();
  Serial.println("STOP");
}


void loggingData()
{
  Serial.print("Tick : "); Serial.println(newPosition);
  Serial.print("Angle : "); Serial.println(angle[measurements - 1]);
  Serial.print("d : "); Serial.println(d, 4);
}


