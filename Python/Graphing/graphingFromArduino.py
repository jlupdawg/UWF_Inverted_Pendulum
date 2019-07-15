import matplotlib.pyplot as plot
import matplotlib.animation as animation
from matplotlib import style

import Controls_Code_Function as Control
import time

import serial

import math

arduino = serial.Serial('COM7', 9600)
print("Connected to : " + arduino.name)

status = 1
lastTime = int(round(time.time() * 1000))
initialTime = lastTime
setPoint = 0
highAngle = 90
oldAngle = 0
Kp = 50
Kd = .1
derivative = 0

style.use('fivethirtyeight')

fig = plot.figure()
anglePlot = fig.add_subplot(1,1,1)

angles = []
anglVes = []
times = []

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

while(1):

    if(status == 1):
        time.sleep(.001)
        angleIn = arduino.readline().strip()
        decodedAngle = angleIn.decode()
        try:
            if(decodedAngle != '\n'):
                angle = int(decodedAngle)
        except:
            continue
        #print("The angle was " + str(angle))

        status, oldAngle , lastTime, derivative = Control.PID(angle, Kp, Kd, highAngle, setPoint, lastTime, oldAngle, status)
        #derivative = roundup(derivative)
        angles.append(angle)
        anglVes.append(derivative)
        times.append(lastTime - initialTime)
    else:
        Control.PID(0)
        anglePlot.plot(times,angles)
        anglePlot.plot(times,anglVes)
        plot.show()
        arduino.close()
        break

