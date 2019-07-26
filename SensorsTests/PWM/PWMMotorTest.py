'''
GND (pin 6) -> GND
PWM (pin 12) -> pins 9 & 10
RightDirection (pin 15) -> pin 7
LeftDirection (pin 16) -> pin 8
'''


import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI

import time                            #calling time to provide delays in program

IO.setwarnings(False)           #do not show any warnings

IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

IO.setup(18,IO.OUT)           # initialize GPIO18 as an output.
IO.setup(22,IO.OUT)
IO.setup(23,IO.OUT)

pwmPin = IO.PWM(18,980)                   #GPIO19 as PWM output, with 980Hz frequency
pwmPin.start(0)                          #generate PWM signal with 0% duty cycle


while 1:
    IO.output(22, 1)
    IO.output(23, 1)
    pwmPin.ChangeDutyCycle(25)
    time.sleep(2)
    IO.output(22, 0)
    IO.output(23, 0)
    time.sleep(2)
    IO.output(22, 1)
    IO.output(23, 1)
    pwmPin.ChangeDutyCycle(50)
    time.sleep(2)
    IO.output(22, 0)
    IO.output(23, 0)
    time.sleep(2)
    IO.output(22, 1)
    IO.output(23, 1)
    pwmPin.ChangeDutyCycle(75)
    time.sleep(2)
    IO.output(22, 0)
    IO.output(23, 0)
    time.sleep(2)
