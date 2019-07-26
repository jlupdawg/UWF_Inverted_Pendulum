'''
Uses HRS04 ultrasonic sensor
vcc -> pin 2 (5 volt)
Trig -> pin 16 (GPI0 23)
Echo -> pin 18 (GPI0 24)
Gnd -> pin 6 (GND)

Voltage divider from Echo to ground to bring input below 3.3V using 1k and 2k resisitors
'''

import RPi.GPIO as GPIO  #imports GPIO library
import time #imports time library

GPIO.setmode(GPIO.BCM)  #defines the pin numberig layout

trig = 23  #Trig is on GPIO 23
echo = 24  #Echo is on GPIO 24

GPIO.setup(trig, GPIO.OUT) #trig is an output
GPIO.setup(echo,GPIO.IN) #echo is an input

while 1:
    GPIO.output(trig, False) #trig LOW
    time.sleep(.1) #delay .1 seconds

    GPIO.output(trig,True) #trig HIGH for .00001 seconds
    time.sleep(.00001)
    GPIO.output(trig,False) #trig LOW

    while GPIO.input(echo)==0: #record signal start time
        pulse_start = time.time()

    while GPIO.input(echo)==1: #record signal stop time
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start 

    if pulse_duration < .1:
        distance = pulse_duration * 17150 / 2.54 #speed of sound constants and cm to in conversion
        distance = round(distance,2) #round to two decinals
    
    print("Distance : " + str(distance) + "IN")

GPIO.cleanup()  #returns all ports used in this code to inputs to prevent damage


