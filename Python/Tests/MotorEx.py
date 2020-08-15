import busio
import board
import time
import encoderTest as coder

from adafruit_pca9685 import PCA9685

print("Initializing PWM")
i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))

pca = PCA9685(i2c_bus0)
pca.frequency = 1600

percent = 35
#coder.initialize_encoder()
time.sleep(5)

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

while int(round(time.time() * 1000)) - start_time < 2000:
    time.sleep(.0001)
    #coder.log_encoder(start_time)

pca.channels[0].duty_cycle = 0
