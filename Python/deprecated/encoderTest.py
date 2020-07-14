import time
import serial
import datetime

serial_port = serial.Serial()

def initialize_port():
    global serial_port
    serial_port = serial.Serial(
        port='/dev/ttyUSB0', #CHANGE ME IF NEEDED
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    )
    # Wait a second to let the port initialize
    time.sleep(1)
    
    file1 = open("encoderData.txt","a")
    file1.write("\n---------------------")
    file1.write(str(datetime.datetime.now))
    file1.write("")
    file1.close()

def initialize_encoder():
    global serial_port
    serial_port.write('g'.encode())
    time.sleep(2.5)

def log_encoder(start_time):
    global serial_port
    file1 = open("encoderData.txt","a")
    data = 0.0
    try:
        #print("Inside try");
        serial_port.flushInput()
        print("Flushed input")
        while True:
            #print("Inside while")
            if serial_port.inWaiting() > 0:
                print("Inside if")
                command = serial_port.read().decode('utf-8')
                #print("Command: ", command)
                if command == 'd':
                    data = serial_port.readline().decode('utf-8')
                    #print("Data: ", data)
                    break
            elif int(round(time.time()*1000)) - start_time > 2000:
                    break
    except:
        pass
    
    if data != 0:
        print("Entered if to write encoder data")
        file1.write(str(int(round(time.time()*1000)) - start_time))
        file1.write("\n")
        file1.write(str(data))
    else:
        print("Skipped if to write encoder data")
    file1.close() 

def close_encoder():
    global serial_port
    serial_port.write('s'.encode())

def close_port():
    global serial_port
    serial_port.close()

def log_encoder_test():
    #Used for serial communication troubleshooting on 5/19/2020
    global serial_port
    #file1 = open("encoderData.txt","a")
    data = 0.0
    command = 'a'
    try:
        print("Inside try");
        serial_port.flushInput()
        print("Flushed input")
        while True:
            #print("Inside while")
            if serial_port.inWaiting() > 0:
                print("Inside if")
                #command = serial_port.read(5).decode('ascii')
                command = serial_port.read().decode('utf-8')
                print("Command: ", command)
                if command == 'd':
                    data = serial_port.readline().decode('utf-8')
                    print("Data: ", data)
                    break
    except:
        pass

    if data != 0:
        print("Entered if to write encoder data")
        #file1.write(str(data))
    else:
        print("Skipped if to write encoder data")
    #file1.close()
    print("Data outside loop");
    print(data)

def read_data():
    global serial_port
    serial_port.write('r'.encode())
    print("Wrote 'r' command to Arduino")
    file1 = open("encoderData.txt","a")
    try:
        i=0
        #while serial_port.inWaiting() > 0:
        while i<200:
            #print("Inside while")
            file1.write(serial_port.readline().decode('utf-8'))
            i = i+1
            #time.sleep(.01)
    except:
        pass
    file1.close() 

def encoder_test():
    #Used for serial communication troubleshooting on 5/19/2020
    initialize_encoder()
    while(True):
        log_encoder_test()
    close_encoder()

if __name__ == '__main__':
    encoder_test()
