from threading import Thread
import serial
import sys

class Encoder:

    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.ang = 0
        self.stopped = False

    def start(self): 
        self.t1 = Thread(target=self.update_ang, args=())   
        self.t1.start()
        return self

    def get_ang(self):
        return self.ang

    def update_ang(self):
        #Read angle from arduino
        self.serial_port.flushInput()
        while self.serial_port.inWaiting() == 0:
            print("Passing")
            pass

        self.ang = int(self.serial_port.readline().decode('utf-8'))
        print("ANGLE: " + self.ang)

    def stop(self):
        print("Dedicated camera thread stopped.")
        self.stopped = True
        self.t1.join()

    def __del__(self):
        self.stop()
