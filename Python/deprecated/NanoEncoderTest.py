#Test for encoder wired to MCP3008 wired to Jetson Nano
#No Serial communication necessary, but circuit-python used to control MCP3008 via SPI

#Libraries for IO
import busio
import digitalio
import board

#Libraries for MCP3008
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#Libraries for motor control
from adafruit_pca9685 import PCA9685

#Libraries for encoder data logging
import time


#Variables
MOTOR_PERCENT = 100
PWM_FREQ = 1600
MAX_TIME = 2 #(in seconds)
MAX_VOLTAGE = 3.3

def main():
	global start_time, start_pos, MOTOR_PERCENT
	initialize()
	time.sleep(1)
	start_time = time.time() * 1000
	start_pos = encoder_channel.voltage / MAX_VOLTAGE * 360
	drive_motor(MOTOR_PERCENT)

	while ((time.time() * 1000 - start_time) < 2000):
		log_data()

	close_all()

def initialize():
	global pca, encoder_channel, file1
	#Initializations for motor control
	i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))
	pca = PCA9685(i2c_bus0)
	pca.frequency = PWM_FREQ

	#Initializations for encoder/MCP3008
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
	cs = digitalio.DigitalInOut(board.D24)
	mcp = MCP.MCP3008(spi, cs)
	encoder_channel = AnalogIn(mcp, MCP.P0)

	#Initialize data logging
	file1 = open("encoderData.txt","a")
	file1.write("PWM Frequency: ")
	file1.write(str(PWM_FREQ))
	file1.write("\nMOTOR SPEED: ")
	file1.write(str(MOTOR_PERCENT))
	file1.write("\n\n")

def drive_motor(percent):
	global pca
	#Set motor to desired PWM signal
	DC = int((percent) * (65534) / (100))
	if DC < 0:
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

def log_data():
	global encoder_channel, MAX_VOLTAGE, start_time, start_pos
	degrees = encoder_channel.voltage / MAX_VOLTAGE * 360
	current_time = time.time() * 1000 - start_time
	file1.write(str(current_time))
	file1.write(" ")
	file1.write(str(degrees - start_pos))
	file1.write("\n")

def close_all():
	global file1
	drive_motor(0)
	file1.close()

if __name__ == "__main__":
	main()

