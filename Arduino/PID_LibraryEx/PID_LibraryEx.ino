/********************************************************
   PID Basic Example
   Reading analog input 0 to control analog PWM output 3
 ********************************************************/

#include <PID_v1.h>
#include <Encoder.h>
#define PIN_OUTPUT 3


Encoder myEnc(20, 21);

//Define Variables we'll be connecting to
double Setpoint, Input, Output;

//Specify the links and initial tuning parameters
double Kp = 100, Ki = 0, Kd = 10; //30, 5 works well for small angles //50,10
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

const int measurements = 1;
long oldPosition = 0;
int angle[measurements];
long newPosition = 0;

const int highAngle = 30; //+- angle of no return

#define rightPWM 9
#define rightDirection 7
#define leftPWM 10
#define leftDirection 8

bool Stat = true;

void setup()
{
  //initialize the variables we're linked to
  Input = 0;
  Setpoint = 0;

  //turn the PID on
  myPID.SetMode(AUTOMATIC);

  Serial.begin(9600);

  pinMode(rightPWM, OUTPUT);
  pinMode(rightDirection, OUTPUT);
  pinMode(leftPWM, OUTPUT);
  pinMode(leftDirection, OUTPUT);
}

void loop()
{
  while (Stat)
  {
    checkEnc();
    Input = angle[measurements - 1];
    myPID.Compute();
    Serial.print("PID Value = "); Serial.println(Output);
    Serial.print("Angle = "); Serial.println(angle[measurements - 1]);
    if (Output < 0)
    {
      forward(-Output);
    }
    else
    {
      backward(Output);
    }
    if ((angle[measurements - 1] > highAngle) || (angle[measurements - 1] < -highAngle))
    {
      Stat = false;
      forward(0);
    }
  }
}


void checkEnc()
{
  newPosition = myEnc.read();
  if (newPosition != oldPosition)
  {
    oldPosition = newPosition;
  }
  for (int i = 0; i < measurements; i++)
  {
    if (i == measurements - 1)
    {
      angle[i] = mapf(newPosition, -510, 510, -360, 360);
    }
    else
    {
      angle[i] = angle[i + 1];
    }
    //Serial.println(angle[i]);
  }
}

float mapf(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (float)(x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}


void forward(float DC)
{
  digitalWrite(leftDirection, HIGH);
  digitalWrite(rightDirection, HIGH);
  analogWrite(leftPWM, DC);
  analogWrite(rightPWM, DC);
  Serial.print("PWM Value = "); Serial.println(DC);
}

void backward(float DC)
{
  digitalWrite(leftDirection, LOW);
  digitalWrite(rightDirection, LOW);
  analogWrite(leftPWM, DC);
  analogWrite(rightPWM, DC);
  Serial.print("PWM Value = "); Serial.println(DC);
}

