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
