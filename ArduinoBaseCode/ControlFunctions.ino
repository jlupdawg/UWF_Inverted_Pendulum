
void derivative(int dt)
{
  checkEnc();
  delayMicroseconds(dt);
  checkEnc();

  d = (float) ((angle[measurements - 1] - angle[measurements - 2]) / (dt * pow(10, -6)));
}
