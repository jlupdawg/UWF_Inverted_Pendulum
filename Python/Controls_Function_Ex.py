import Controls_Code_Function as Control
import time
#PID(angle, Kp, Kd, highAngle, setPoint, lastTime, oldAngle)
#return stat, oldAngle, lastTime

status = 1
lastTime = int(round(time.time() * 1000))
setPoint = 0
highAngle = 30
oldAngle = 0
Kp = 50
Kd = 10

while(1):
    if(status == 1):
        try:
            angle = float(input('Please input an angle : '))
        except:
            continue
        status, oldAngle , lastTime = Control.PID(angle, Kp, Kd, highAngle, setPoint, lastTime, oldAngle, status)
    else:
        Control.PID(0)
