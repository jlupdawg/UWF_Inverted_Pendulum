import time
import datetime

Kp = 50
Kd = 10
highAngle = 30
stat = 1
PWMLimit = 255
setPoint = 0
oldAngle = 0
lastTime = int(round(time.time() * 1000))

def getAngle():
    #get the angle from the Jetson Nano
    degrees = input('Angle = ')
    degrees = int(degrees)
    return degrees

def forward(speed):
    #Code to make the motors go foward PWM and GPIO
    print("Foward at " + str(speed) + " speed")

def backward(speed):
    #Code to make the motors go foward PWM and GPIO
    print("Backward at " + str(speed) + " speed")

def control(angle, derive):
    PD = Kp*(angle-setPoint) + Kd*derive
    if(PD < 0):
        PD = max(-PWMLimit, PD)
        PD = -PD
        backward(PD)
    elif(PD >= 0):
        PD = min(PD, PWMLimit)
        forward(PD)
        
def derivative(new, last, thisTime, lastTime):
    dt = thisTime - lastTime
    print(dt)
    derive = (new - last)/(dt/1000)
    lastTime = thisTime
    return derive
    
while(stat == 1):
    try:
        angle = getAngle()
    except:
        continue
    thisTime = int(round(time.time() * 1000))
    derive = derivative(angle, oldAngle,thisTime, lastTime)
    lastTime = thisTime
    control(angle, derive)
    if(angle > highAngle or angle < -highAngle):
        stat = 0
    oldAngle = angle
