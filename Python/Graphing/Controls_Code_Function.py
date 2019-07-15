import time

PWMLimit = 255

def forward(speed):
    #Code to make the motors go foward PWM and GPIO
    print("Forward at " + str(speed) + " speed")

def backward(speed):
    #Code to make the motors go foward PWM and GPIO
    print("Backward at " + str(speed) + " speed")
        
def derivative(new, last, thisTime, lastTime):
    dt = thisTime - lastTime
    derive = (new - last)/(dt/1000)
    lastTime = thisTime
    return derive

def PID(angle, Kp = 50, Kd = 0, highAngle = 30, setPoint = 0, lastTime = 0, oldAngle = 0, stat = 0):

    thisTime = int(round(time.time() * 1000))
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
