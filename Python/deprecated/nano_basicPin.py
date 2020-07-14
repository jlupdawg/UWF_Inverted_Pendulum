import sys
sys.path.append('/opt/nvidia/jetson-gpio/lib/python')
import RPi.GPIO as GPIO          #calling header file which helps us use GPIOs of PI
import time                            #calling time to provide delays in program
output_pin = 33
if output_pin is None:
    raise Exception('PWM not supported on this board')

def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT)

    print("Pulse Code running. Press CTRL+C to exit.")
    try:
        while True:
            GPIO.output(output_pin, 1)
            time.sleep(1)
            GPIO.output(output_pin, 0)
            time.sleep(1)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
