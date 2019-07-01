
void forward(float DC)
{
  DC = PD*maxMotorPWM;
  digitalWrite(leftDirection, HIGH);
  digitalWrite(rightDirection, HIGH);
  analogWrite(leftPWM, DC);
  analogWrite(rightPWM, DC);
  Serial.print("PWM Value = "); Serial.println(DC);
}

void backward(float DC)
{
  DC = PD*maxMotorPWM;
  digitalWrite(leftDirection, LOW);
  digitalWrite(rightDirection, LOW);
  analogWrite(leftPWM, DC);
  analogWrite(rightPWM, DC);
  Serial.print("PWM Value = ");Serial.println(DC);
}

void Stop()
{
  digitalWrite(leftDirection, LOW);
  digitalWrite(rightDirection, LOW);
  analogWrite(leftPWM, 0);
  analogWrite(rightPWM, 0);
}



