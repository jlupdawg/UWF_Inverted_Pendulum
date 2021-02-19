from threading import Thread
import serial
import sys
import time

class SerialThread:

    def __init__(self, serial_port):
        #self.serial_port = serial_port
        self.serial_port = serial.Serial(
		port='/dev/ttyUSB0', #CHANGE ME IF NEEDED
		baudrate=115200,
		bytesize=serial.EIGHTBITS,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		)
        time.sleep(1)
        self.serial_port.write('s'.encode())
        self.pos = 0
        self.stopped = False
        time.sleep(0.01)
        self.serial_port.write('r'.encode())
        while self.serial_port.inWaiting() == 0:
            #print("INNER WHILE LOOP -----")
            pass
        self.pos = (self.serial_port.readline().rstrip()).decode('utf-8')

    def start(self): 
        self.t1 = Thread(target=self.update_pos, args=())   
        self.t1.start()
        print("Started Thread -------------- :)")
        return self

    def get_pos(self):
        return self.pos

    def update_pos(self):
        print("Called Update Pos ----- :)")
        #Read position from arduino
        while not self.stopped:
            if True:
                self.serial_port.write('r'.encode())
                while self.serial_port.inWaiting() == 0:
                    #print("INNER WHILE LOOP -----")
                    pass
                self.pos = (self.serial_port.readline().rstrip()).decode('utf-8')
                #print("Updating Pos : ", self.pos)
               

    def stop(self):
        print("Dedicated camera thread stopped.")
        self.serial_port.close()
        self.stopped = True
        self.t1.join()

    def __del__(self):
        self.stop()
