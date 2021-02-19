#IMPORTS
import busio
import board
from adafruit_pca9685 import PCA9685 #import the library for the digital to PWM converter
import serial
import time
import SerialThread

class Motors():
    def __init__(self, max_pwm=85, frequency=50, arduino_port='/dev/ttyUSB0'):
        self.max_pwm = max_pwm

        #PWM Controller Initialization
        print("Initializing PWM") #It takes a second to initialize... let the user know
        self.i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1)) #Creates the i2c bus to control the converter
        self.pca = PCA9685(self.i2c_bus0)
        self.pca.frequency = frequency #Frequency = 50 hz... this may need changing for optimizing the motors

        #Serial port communication initialization
        '''self.serial_port = serial.Serial(
        	port=arduino_port, #CHANGE ME IF NEEDED
        	baudrate=115200,
        	bytesize=serial.EIGHTBITS,
        	parity=serial.PARITY_NONE,
        	stopbits=serial.STOPBITS_ONE,
	        )'''

        self.serial_thread = SerialThread.SerialThread(None)
        self.serial_thread.start()
        # Wait a second to let the port initialize
        time.sleep(1)
        self.pos = 0
        
    def forward(self, DC):
        DC = min(self.max_pwm, DC)  # Constrain motor speed
        ###print("Forward at " + str(DC) + " speed")  #For inspection purposes
        
        DC = int((DC) * (65534) / (100)) #Convert the duty cycle from a percent 0-100 to a percent of MAXINT
        self.pca.channels[1].duty_cycle = 0  #direction to forward in HEX
        DC = int(hex(DC),16)  #make DC into HEX for the library

        try:
            self.pca.channels[0].duty_cycle = DC
        except:
            self.pca.channels[0].duty_cycle = 0
    

    def backward(self, DC):
        DC = min(self.max_pwm, DC)  # Constrain motor speed
        ###print("Backward at " + str(DC) + " speed")
        
        DC = int((DC) * (65534) / (100)) 
        self.pca.channels[1].duty_cycle = 0xFFFE #direction to backward in HEX
        DC = int(hex(DC),16)  #make DC into HEX for the library
    
        try:
            self.pca.channels[0].duty_cycle = DC
        except:
            self.pca.channels[0].duty_cycle = 0

    def get_pos(self):
        #print("Calling Motors")
        self.pos = self.serial_thread.get_pos()
        return self.pos

    def close(self):
        self.serial_thread.stop()
