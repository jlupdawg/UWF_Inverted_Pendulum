/*  Honeywell 600EN-128-CBL
  Red, 5V
  Orange, D20 (Must be a hardware interrupt pin)
  Yellow, D21 (Must be a hardware interrupt pin)
  Green, Ground
*/

#include <Encoder.h>

Encoder myEnc(20, 21);

const int measurements = 1;
long oldPosition = 0;
int angle[measurements];
long newPosition = 0;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
    checkEnc();
    delay(80);
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
    Serial.println(angle[i]);
  }
}

float mapf(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (float)(x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}



