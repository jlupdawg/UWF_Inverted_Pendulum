import time
import Jetson.GPIO as GPIO
import rotary_encoder

A_PIN = 18
B_PIN = 13
deg = 0

gpio = GPIO
GPIO.setmode(GPIO.BOARD)
encoder = rotary_encoder.RotaryEncoder(gpio, A_PIN, B_PIN)
encoder.start()
while True:
  delta = encoder.get_cycles()
  deg += delta
  if delta!=0:
    print(str(deg))
  else:
    time.sleep(0.01)
