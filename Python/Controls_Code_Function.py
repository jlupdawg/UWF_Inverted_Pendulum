import sys
sys.path.append('/home/nano-pendulum/.local/lib/python3.6/site-packages/')

import busio

import time
import board
import time

from adafruit_pca9685 import PCA9685

print("Initializing PWM")
i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))

pca = PCA9685(i2c_bus0)
pca.frequency = 50
PWMLimit = 100

def forward(DC):
    DC = int((DC) * (65534) / (100))
    pca.channels[1].duty_cycle = 0  #direction to forward
    DC = int(hex(DC),16)  #make DC into HEX for the library
    try:
        pca.channels[0].duty_cycle = DC
    except:
        pca.channels[0].duty_cycle = 0
    print("Forward at " + str(DC) + " speed")

def backward(DC):
    DC = int((DC) * (65534) / (100))
    pca.channels[1].duty_cycle = 1  #direction to backward
    DC = int(hex(DC),16)  #make DC into HEX for the library
    try:
        pca.channels[0].duty_cycle = DC
    except:
        pca.channels[0].duty_cycle = 0
    print("Backward at " + str(DC) + " speed")
        
def derivative(new, last, thisTime, lastTime):
    dt = thisTime - lastTime
    #print ("DT = " + str(dt))
    derive = (new - last)/(float(dt)/1000)
    #print("Derivative = " + str(derive))
    return derive

def PID(angle, Kp = 50, Kd = 0, highAngle = 30, setPoint = 0, lastTime = 0, oldAngle = 0, stat = 0):

    thisTime = int(round(time.time() * 1000))
    #print ("This Time = " + str(thisTime))
    derive = derivative(angle, oldAngle,thisTime, lastTime)
    lastTime = thisTime

    PD = Kp*(angle-setPoint) + Kd*derive
    if(PD < 0):
        PD = max(-PWMLimit, PD)
        PD = -PD
        backward(PD)
    elif(PD >= 0):
        PD = min(PD, PWMLimit)
        forward(PD)

    if(angle > highAngle or angle < -highAngle):
        stat = 0
    oldAngle = angle
        
    return stat, oldAngle, lastTime, derive
