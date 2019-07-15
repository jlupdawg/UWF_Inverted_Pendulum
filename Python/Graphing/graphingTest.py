import matplotlib.pyplot as plot
import matplotlib.animation as animation
from matplotlib import style

import Controls_Code_Function as Control
import time

status = 1
lastTime = int(round(time.time() * 1000))
initialTime = lastTime
setPoint = 0
highAngle = 30
oldAngle = 0
Kp = 50
Kd = 10
derivative = 0

style.use('fivethirtyeight')

fig = plot.figure()
anglePlot = fig.add_subplot(1,2,1)

angles = []
anglVes = []
time = []


while(1):
    if(status == 1):
        try:
            angle = float(input('Please input an angle : '))
        except:
            continue
        status, oldAngle , lastTime, derivative = Control.PID(angle, Kp, Kd, highAngle, setPoint, lastTime, oldAngle, status)
        print(derivative)
        angles.append(angle)
        anglVes.append(derivative)
        time.append(lastTime - initialTime)
    else:
        Control.PID(0)
        anglePlot.plot(time,angles)
        anglePlot.plot(time,anglVes)
        plot.show()
        break

