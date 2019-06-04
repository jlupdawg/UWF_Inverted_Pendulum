
void forward(int DC)
{
  DC = PD*maxMotorPWM;
  digitalWrite(leftDirection, HIGH);
  digitalWrite(rightDirection, HIGH);
  analogWrite(leftPWM, DC);
  analogWrite(rightPWM, DC);
}

void backward(int DC)
{
  DC = PD*maxMotorPWM;
  digitalWrite(leftDirection, LOW);
  digitalWrite(rightDirection, LOW);
  analogWrite(leftPWM, DC);
  analogWrite(rightPWM, DC);
}

void Stop()
{
  digitalWrite(leftDirection, LOW);
  digitalWrite(rightDirection, LOW);
  analogWrite(leftPWM, 0);
  analogWrite(rightPWM, 0);
}



