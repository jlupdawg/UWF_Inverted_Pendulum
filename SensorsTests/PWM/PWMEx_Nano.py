import sys
sys.path.append('/opt/nvidia/jetson-gpio/lib/python')

import Jetson.GPIO as GPIO          #calling header file which helps us use GPIOs of PI
import time                            #calling time to provide delays in program
'''
output_pins = {
    'JETSON_XAVIER': 18,
    'JETSON_NANO': 33,
}
'''
output_pin = 33
if output_pin is None:
    raise Exception('PWM not supported on this board')

def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)
    p = GPIO.PWM(output_pin, 100)
    p.start(50)

    print("PWM running. Press CTRL+C to exit.")
    try:
        while True:
           time.sleep(.1)
    finally:
        p.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()
