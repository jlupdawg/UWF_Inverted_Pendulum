#Similar to MotorEx except it reads all Serial data after the motors have stopped
#Must be used with ThroughShaftEncoder2 Arduino sketch

import busio
import board
import time
import encoderTest as coder

from adafruit_pca9685 import PCA9685

#Initialize PWM and Motor Setup
print("Initializing PWM")
i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))

pca = PCA9685(i2c_bus0)
pca.frequency = 1600

percent = 80

#Initialize Port
coder.initialize_port()
time.sleep(3)

#Tell the Arduino to start recording encoder data
coder.initialize_encoder()

#Set motor to desired PWM signal
DC = int((percent) * (65534) / (100))
if DC < 0:
    DC = -DC
    pca.channels[1].duty_cycle = 0xFFFE
else:
    pca.channels[1].duty_cycle = 0

DC = int(hex(DC),16)
try:
    print("Setting motors to ")
    print(DC)
    pca.channels[0].duty_cycle = DC
except:
    pca.channels[0].duty_cycle = 0

start_time = int(round(time.time() * 1000))

#Wait 1 second
while int(round(time.time() * 1000)) - start_time < 1000:
    pass

#Turn off motors, wait, and stop reading encoder data
pca.channels[0].duty_cycle = 0
time.sleep(0.5)
coder.close_encoder()

#Receive all serial code to data
coder.read_data()
coder.close_port()
