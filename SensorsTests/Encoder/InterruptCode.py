
#!/usr/bin/env python2.7  
# script by Alex Eames https://raspi.tv  
# https://raspi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3  
import RPi.GPIO as GPIO
import time as time
GPIO.setmode(GPIO.BCM)  
  
# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.  
# Both ports are wired to connect to GND on button press.  
# So we'll be setting up falling edge detection for both  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
  
# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press  
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
  
# now we'll define two threaded callback functions  
# these will run in another thread when our events are detected  
def my_callback(channel):  
    print ("falling edge detected on 22" ) 
  
def my_callback2(channel):  
    print ("falling edge detected on 23" ) 
    

# when a falling edge is detected on port 23, regardless of whatever   
# else is happening in the program, the function my_callback2 will be run  
# 'bouncetime=300' includes the bounce control written into interrupts2a.py  
GPIO.add_event_detect(22, GPIO.FALLING, callback=my_callback2, bouncetime=300)  
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback, bouncetime=300)
while 1:
    time.sleep(.1)
 
