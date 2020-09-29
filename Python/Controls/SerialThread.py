from threading import Thread
import serial
import sys

class SerialThread:

    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.serial_port.write('s'.encode())
        self.pos = 0
        self.stopped = False

    def start(self): 
        self.t1 = Thread(target=self.update_pos, args=())   
        self.t1.start()
        return self

    def get_pos(self):
        return self.pos

    def update_pos(self):
        #Read position from arduino
        self.serial_port.write('r'.encode())
        while self.serial_port.inWaiting() == 0:
            pass

        self.pos = int(self.serial_port.readline().decode('utf-8')) / 1000 * 2 * 3.141592 * 0.05 #Read degrees and convert to meters

    def stop(self):
        print("Dedicated camera thread stopped.")
        self.stopped = True
        self.t1.join()

    def __del__(self):
        self.stop()
