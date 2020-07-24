import RPi.GPIO as GPIO
import busio
import board
from adafruit_pca9685 import PCA9685
import serial

import time
from datetime import datetime

# Pin Definitions:
CHAN_A = 18
CHAN_B = 13

#Encoder definition
direc = 1 #1 for forward, -1 for backward
pos = 0

#Motor speed %
percent = 75
max_dist = 8000

#Serial communications
serial_port = serial.Serial()

'''def increment_pos(CHAN_A):
	global pos
	pos += direc'''

def main():
	global CHAN_A, CHAN_B, percent, pos, serial_port, max_dist
	# Pin/Encoder Setup:
	GPIO.cleanup()
	GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
	'''GPIO.setup([CHAN_A,CHAN_B], GPIO.IN)
	GPIO.add_event_detect(CHAN_A, GPIO.RISING, callback=increment_pos)'''

	#Serial port communication initialization
	serial_port = serial.Serial(
		port='/dev/ttyUSB0', #CHANGE ME IF NEEDED
		baudrate=115200,
		bytesize=serial.EIGHTBITS,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		)
    	# Wait a second to let the port initialize
	time.sleep(1)
	serial_port.write('s'.encode())
	pos = 0

	#Data logging
	file1 = open("encoderData.txt","a")
	file1.write("\n---------------------\n")
	file1.write("Encoder velocity testing.\n")
	file1.write(str(percent) + "%")
	file1.write("\n---------------------\n")

	#Motor handling
	print("Initializing PWM")
	i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))

	pca = PCA9685(i2c_bus0)
	pca.frequency = 1600

	time.sleep(3)

	#Motor control
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

	#Encoder reading
	try:
		#Read and log encoder for n seconds
		prev_micros = curr_micros = 0.0
		prev_pos = 0
		#while int(round(time.time() * 1000)) - start_time < 2000:
		while int(pos) < max_dist:
			curr_micros = datetime.now().second * 1000000 + datetime.now().microsecond
			if curr_micros != prev_micros:
				serial_port.write('r'.encode())
				print("Sending r")
				while serial_port.inWaiting() == 0:
					pass
				pos = serial_port.readline().decode('utf-8')

				if pos != prev_pos:
					print(pos)
					prev_micros = curr_micros
					prev_pos = pos
					file1.write(str(curr_micros) + " ")
					file1.write(str(pos))
					file1.write("")
			
	finally:
		#Cleanup
		pca.channels[0].duty_cycle = 0
		file1.close()
		time.sleep(0.5)
		GPIO.cleanup()
		serial_port.close()

if __name__ == '__main__':
	main()
