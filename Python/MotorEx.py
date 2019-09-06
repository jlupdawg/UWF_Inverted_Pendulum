import busio
import board
import time

from adafruit_pca9685 import PCA9685

print("Initializing PWM")
i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))

pca = PCA9685(i2c_bus0)
pca.frequency = 50

percent = 50

while 1:
    DC = int((percent) * (65534) / (100))
    if DC < 0:
        DC = -DC
        pca.channels[1].duty_cycle = 0xFFFE
    else:
        pca.channels[1].duty_cycle = 0

    DC = int(hex(DC),16)
    try:
        pca.channels[0].duty_cycle = DC
    except:
        pca.channels[0].duty_cycle = 0
        continue
    time.sleep(1)
    percent = -percent

