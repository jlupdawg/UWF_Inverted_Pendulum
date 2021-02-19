import Encoder
import serial
import time

encoder_port = '/dev/ttyUSB0'

#Serial port communication initialization
enc_port = serial.Serial(
	port=encoder_port, #CHANGE ME IF NEEDED
	baudrate=57200,
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	)

encoder_thread = Encoder.Encoder(enc_port)
encoder_thread.start()
# Wait a second to let the port initialize
time.sleep(1)
angle = 0

while(1):
	angle = encoder_thread.get_ang()
	print(angle)
