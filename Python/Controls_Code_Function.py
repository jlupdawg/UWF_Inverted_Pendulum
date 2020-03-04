import sys 
sys.path.append('/home/nano-pendulum/.local/lib/python3.6/site-packages/') ##Adds another possible path for header files

import busio

import time
import board
#second import time was here... REMOVED "#import time"

from adafruit_pca9685 import PCA9685 #import the library for the digital to PWM converter

print("Initializing PWM") #It takes a second to initialize... let the user know
i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1)) #Creates the i2c bus to control the converter

pca = PCA9685(i2c_bus0)
pca.frequency = 50 #Frequency = 50 hz... this may need changing for optimizing the motors
PWMLimit = 100 # The maximum value for PWM is 100 to make conversions easy

def forward(DC):
    print("Forward at " + str(DC) + " speed")  #For inspection purposes
    DC = int((DC) * (65534) / (100)) #Convert the duty cycle from a percent 0-100 to a percent of MAXINT
    pca.channels[1].duty_cycle = 0  #direction to forward 
    DC = int(hex(DC),16)  #make DC into HEX for the library
    try:
        pca.channels[0].duty_cycle = DC #try to write the pwm value
    except:
        pca.channels[0].duty_cycle = 0 #if something is wrong stop the system
    

def backward(DC):
    print("Backward at " + str(DC) + " speed")
    DC = int((DC) * (65534) / (100)) 
    pca.channels[1].duty_cycle = 0xFFFE #direction to backward in HEX
    DC = int(hex(DC),16)  #make DC into HEX for the library
    try:
        pca.channels[0].duty_cycle = DC
    except:
        pca.channels[0].duty_cycle = 0

def derivative(new, last, thisTime, lastTime): #Find the derivative of theta
    dt = thisTime - lastTime
    #print ("DT = " + str(dt))
    derive = (new - last)/(float(dt)/1000) 
    #print("Derivative = " + str(derive))
    return derive

def PID(angle, Kp = 50, Kd = 0, highAngle = 30, setPoint = 0, lastTime = 0, oldAngle = 0, stat = 0):
    thisTime = int(round(time.time() * 1000)) #get the current time
    #print ("This Time = " + str(thisTime))
<<<<<<< HEAD
    derive = derivative(angle, oldAngle,thisTime, lastTime)
    lastTime = thisTime
    print("Kp : " + str(Kp) + "	Angle : " + str(angle-setPoint))
    print("Kd : " + str(Kd) + "	Derivative : " + str(derive))
    PD = Kp*(angle-setPoint) + Kd*derive
    PDorg = PD
=======
    derive = derivative(angle, oldAngle,thisTime, lastTime) #find the derivative
    lastTime = thisTime #set the time for the next derivative
    print("Kp : " + str(Kp) + "	Angle : " + str(angle-setPoint)) #For data analysis
    print("Kd : " + str(Kd) + "	Derivative : " + str(derive)) #For data analysis
    PD = Kp*(angle-setPoint) + Kd*derive #PD = Kp*Theta + Kd*Theta dot
>>>>>>> e226ccaa5ca85fe07d3d359388ba10fcc88f7c0b
    if(PD < 0):
        PD = max(-PWMLimit, PD)
        PD = -PD
        backward(PD)
    elif(PD >= 0):
        PD = min(PD, PWMLimit)
        forward(PD)

    if(angle > highAngle or angle < -highAngle):
<<<<<<< HEAD
        stat = 0
    oldAngle = angle

    if(PDorg > 100):
        PDorg = 100
    elif(PDorg < -100):
        PDorg = -100
        
    return stat, oldAngle, lastTime, derive, PDorg
=======
        stat = 0  #Stops the car if the angle is too large
    oldAngle = angle #Record this for the deriative
        
    return stat, oldAngle, lastTime, derive #Return important data
>>>>>>> e226ccaa5ca85fe07d3d359388ba10fcc88f7c0b
