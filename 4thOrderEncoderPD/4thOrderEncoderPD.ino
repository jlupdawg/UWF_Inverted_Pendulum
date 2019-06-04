/*  Honeywell 600EN-128-CBL
  Red, 5V
  Orange, D20 (Must be a hardware interrupt pin)
  Yellow, D21 (Must be a hardware interrupt pin)
  Green, Ground
*/

#include <Encoder.h>

Encoder myEnc(20, 21);


long oldPosition = 0;
const int measurements = 3;
int angle[measurements];
long newPosition = 0;
float k = 0;
float d = 0;

int deadZone = 1; //+-angle where action will not occur
int highAngle = 60; //+- angle of no return

int lowV = 0;
int highV = 1000;

unsigned long currentTime = 0;
unsigned long lastTime = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  D(10000); //Delay in microseconds
  P();

  for (int i = 0; i < measurements; i++)
  {
    Serial.print(angle[i]);
  }
  Serial.println();
}

void PID()
{
  
}
void P()
{
  k = (float) abs(angle[measurements - 1]) / (highAngle - deadZone);
  k = max(k, .2);
  k = min(k, 1);
  Serial.print("k = "); Serial.println(k, 4);
}

void D(int dt)
{
  checkEnc();
  delayMicroseconds(dt);
  checkEnc();
  delayMicroseconds(dt);
  checkEnc();

  d = (float) ((3 * angle[measurements - 1] - 4 * angle[measurements - 2] + angle[measurements - 3]) / (2 * (dt * pow(10, -6))));
  Serial.print("d = "); Serial.println(d, 4);
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
      angle[i] = map(newPosition, -510, 510, -360, 360);
    }
    else
    {
      angle[i] = angle[i + 1];
    }
  }
}



