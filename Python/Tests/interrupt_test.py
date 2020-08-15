import RPi.GPIO as GPIO
import time
from datetime import datetime

# Pin Definitions:
CHAN_A = 18
CHAN_B = 13

a_val = 0
b_val = 0

A = B = Old = New = 0

def increment_A(CHAN_A):
	global a_val
	a_val += 1
	print(a_val)
	'''print("A,",GPIO.input(CHAN_A))
	print("B,",GPIO.input(CHAN_B))'''
	'''if GPIO.input(CHAN_B):
		a_val -= 1
	else:
		a_val += 1'''
	'''A = 1
	if GPIO.input(CHAN_B) == 0:
		a_val += 1
	else:
		a_val -= 1
	print("A:",a_val)'''

def increment_B(CHAN_B):
	global a_val, A, B
	pass
	'''B = 1
	if A == 0:
		a_val -= 1
	else:
		A = B = 0
	print("B:",a_val)'''

def main():
	global a_val, b_val
	# Pin Setup:
	GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
	GPIO.setup([CHAN_A,CHAN_B], GPIO.IN)

	GPIO.add_event_detect(CHAN_A, GPIO.RISING, callback=increment_A)
	#GPIO.add_event_detect(CHAN_B, GPIO.RISING, callback=increment_B)

	try:
		while True:
			'''print("Waiting")
			GPIO.wait_for_edge(18, GPIO.RISING)
			print("Done waiting")'''

			#print(a_val)
			pass

			'''value1 = GPIO.input(CHAN_A)
			if value1 == GPIO.HIGH:
				value_str1 = "HIGH"
				print("high")
			else:
				value_str1 = "LOW"
				print("low")
			print("Value read from pin {} : {}".format(CHAN_A,
		                                                   value_str1))'''
	finally:
		GPIO.cleanup()

if __name__ == '__main__':
	main()
