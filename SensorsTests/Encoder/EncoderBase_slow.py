'''
Reading Honeywell 600EN-128-CN1
Red -> pin 2 (5 Volt)
yellow -> pin 15 (GPIO22)
Orange -> pin 16 (GPIO23)
Green -> pin 6 (GND)
'''
import RPi.GPIO as GPIO
import time as time
GPIO.setmode(GPIO.BCM)

flagA = 0
flagB = 0
counter = 0
  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

   
def CallBack22(channel):
    global flagA
    global flagB
    
    status = GPIO.input(22)
    print ("Pin 22 is " + str(status))
    if(status == 0):
        flagA = 1
    elif(status == 1):
        flagA = 2
        
    if(flagB == 1):
        if(flagA == 1):
            countDown()
            flagA = flagB = 0
    if(flagB == 2):
        if(flagA == 2):
            countDown()
            flagA = flagB = 0

  
def CallBack23(channel):
    global flagA
    global flagB
    
    status = GPIO.input(23)
    print ("Pin 23 is " + str(status))
    
    if(status == 0):
        flagB = 1
    elif(status == 1):
        flagB = 2
        
    if(flagA == 1):
        if(flagB == 1):
            countUp()
            flagA = flagB = 0
    if(flagA == 2):
        if(flagB == 2):
            countUp()
            flagA = flagB = 0

def countUp():
    global counter
    counter = counter+1
    print(counter)
    
def countDown():
    global counter
    counter = counter-1
    print(counter)

     
GPIO.add_event_detect(22, GPIO.BOTH, callback=CallBack22, bouncetime=1)  
GPIO.add_event_detect(23, GPIO.BOTH, callback=CallBack23, bouncetime=1)

def loop():
    global flagA
    global flagB
    global counter
   

while 1:
    loop()
