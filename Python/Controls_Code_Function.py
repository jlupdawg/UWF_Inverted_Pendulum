import sys 
sys.path.append('/home/nano-pendulum/.local/lib/python3.6/site-packages/') ##Adds another possible path for header files

import busio
import time
import board

from adafruit_pca9685 import PCA9685 #import the library for the digital to PWM converter

#PWM Controller Initialization
print("Initializing PWM") #It takes a second to initialize... let the user know
i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1)) #Creates the i2c bus to control the converter

pca = PCA9685(i2c_bus0)
pca.frequency = 50 #Frequency = 50 hz... this may need changing for optimizing the motors
PWMLimit = 100 # The maximum value for PWM is 100 to make conversions easy

#Global Variable Initialization
curr_time = prev_time = 0
prev_x = prev_theta = 0
max_theta = 30
max_pwm = 85 #Max desired motor percent
pwm_offset = 16.67

def forward(DC):
    DC = min(max_pwm, DC)  # Constrain motor speed
    print("Forward at " + str(DC) + " speed")  #For inspection purposes

    DC = int((DC) * (65534) / (100)) #Convert the duty cycle from a percent 0-100 to a percent of MAXINT
    pca.channels[1].duty_cycle = 0  #direction to forward 
    DC = int(hex(DC),16)  #make DC into HEX for the library

    try:
        pca.channels[0].duty_cycle = DC #try to write the pwm value
    except:
        pca.channels[0].duty_cycle = 0 #if something is wrong stop the system
    

def backward(DC):
    DC = min(max_pwm, DC)  # Constrain motor speed
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
    derive = (new - last)/(float(dt)/1000)
    return derive

def LQR(theta, x, K=[1,1,1,1], set_pt_theta = 0, set_pt_x = 0, stat = 0):
    global curr_time, prev_time, max_theta, pwm_offset

    if (theta > max_theta or theta < -max_theta):
        forward(0)
        stat = 0
        return

    curr_time = int(round(time.time() * 1000))  # get the current time
    theta_dot = derivative(theta, prev_theta, curr_time, prev_time)
    x_dot = derivative(x, prev_x, curr_time, prev_time)

    prev_time = curr_time
    prev_theta = theta
    prev_x = x

    states = [(x-set_pt_x), x_dot, theta, theta_dot]
    duty_cycle = sum([states[i]*k[i] for i in range(len(k))])

    if duty_cycle > 0:
        forward(duty_cycle + pwm_offset)
    else:
        backward(-duty_cycle + pwm_offset)

    return stat

def PID(angle, Kp = 50, Kd = 0, highAngle = 30, setPoint = 0, lastTime = 0, oldAngle = 0, stat = 0):
    thisTime = int(round(time.time() * 1000)) #get the current time
    #print ("This Time = " + str(thisTime))
    derive = derivative(angle, oldAngle,thisTime, lastTime)
    lastTime = thisTime
    print("Kp : " + str(Kp) + "	Angle : " + str(angle-setPoint))
    print("Kd : " + str(Kd) + "	Derivative : " + str(derive))
    PD = Kp*(angle-setPoint) + Kd*derive
    PDorg = PD
    derive = derivative(angle, oldAngle,thisTime, lastTime) #find the derivative
    lastTime = thisTime #set the time for the next derivative
    print("Kp : " + str(Kp) + "	Angle : " + str(angle-setPoint)) #For data analysis
    print("Kd : " + str(Kd) + "	Derivative : " + str(derive)) #For data analysis
    PD = Kp*(angle-setPoint) + Kd*derive #PD = Kp*Theta + Kd*Theta dot
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

    if(PDorg > 100):
        PDorg = 100
    elif(PDorg < -100):
        PDorg = -100
        
    return stat, oldAngle, lastTime, derive, PDorg