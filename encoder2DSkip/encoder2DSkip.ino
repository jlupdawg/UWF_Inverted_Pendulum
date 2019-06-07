/*  Honeywell 600EN-128-CBL
  Red, 5V
  Orange, D20 (Must be a hardware interrupt pin)
  Yellow, D21 (Must be a hardware interrupt pin)
  Green, Ground
*/

#include <Encoder.h>

Encoder myEnc(20, 21);


long oldPosition = 0;
const int measurements = 5;
float angle[measurements];
long newPosition = 0;
float k = 0;
float d2 = 0;


int deadZone = 1; //+-angle where action will not occur
int highAngle = 60; //+- angle of no return

unsigned long currentTime = 0;
unsigned long lastTime = 0;

int del = 8000;
long dt = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  currentTime = millis();
  for(int i = 0; i < measurements; i++)
  {
  checkEnc();
  delayMicroseconds(del);
  }
  dt = (currentTime - lastTime) * 1000;
  D2();
  lastTime = currentTime;
  Serial.print(angle[measurements - 1]); Serial.print(",");Serial.println(d2);
  //Serial.println(dt);
}
void D2()
{
  d2 = (float)((3 * angle[0] - 4 * angle[(measurements-1)/2] + angle[measurements - 1]) / (2 * (dt * pow(10, -6))));
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


float mapf(long x, long in_min, long in_max, long out_min, long out_max)
{
  return (float)(x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
