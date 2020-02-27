import time
import serial
import datetime

def initilize_encoder():
    serial_port = serial.Serial(
        port="/dev/ttyTHS1",
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    )
    # Wait a second to let the port initialize
    time.sleep(1)
    
    file1.open("encoderData.txt","a")
    file1.write("\n---------------------")
    file1.write(str(datetime.datetime.now))
    file1.write("")

def log_encoder():
    try:
        serial_port.flushInput()
        while True:
            if serial_port.inWaiting() > 0:
                data = serial_port.read()
                break
    except:
        pass
            
    file1.write(data)
    


def close_encoder():
    serial_port.close()
    file1.close()
