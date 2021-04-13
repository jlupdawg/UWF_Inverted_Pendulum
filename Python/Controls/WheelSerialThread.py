from threading import Thread
import serial
import sys
import time


class WheelSerialThread:

    def __init__(self):
        # self.serial_port = serial_port
        self.serial_port = serial.Serial(
            port='/dev/arduino_top',  # CHANGE ME IF NEEDED
            baudrate=115200,
            # baudrate=57600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        time.sleep(1)
        self.pos = 0.0
        self.offset = -1.0
        self.stopped = False

    def start(self):
        if True:
            while (self.offset != 0.0):
                self.serial_port.write('s'.encode())
                self.serial_port.write('r'.encode())
                counter = 0
                while self.serial_port.inWaiting() == 0:
                    # print("INNER WHILE LOOP -----")
                    time.sleep(0.0001)
                    if counter >= 5:
                        self.serial_port.write('r'.encode())
                        counter = 0
                    counter = counter + 1
                line = self.serial_port.readline().rstrip()
                self.offset = float(line.decode('utf-8'))
                # print("Updating Pos : ", self.pos)

        self.t1 = Thread(target=self.update_pos, args=())
        self.t1.start()
        # print("Started Thread -------------- :)")
        return self

    def get_pos(self):
        print("Gotten pos: ", self.pos)
        return self.pos * 0.1 / 360

    def update_pos(self):
        counter = 0
        while not self.stopped:
            if True:
                self.serial_port.write('r'.encode())
                while self.serial_port.inWaiting() == 0:
                    # print("INNER WHILE LOOP -----")
                    time.sleep(0.0001)
                    if counter >= 5:
                        self.serial_port.write('r'.encode())
                        counter = 0
                    counter = counter + 1
                line = self.serial_port.readline().rstrip()
                self.pos = float(line.decode('utf-8'))
            time.sleep(0.0001)

    def stop(self):
        print("Dedicated camera thread stopped.")
        self.serial_port.close()
        self.stopped = True
        self.t1.join()

    def __del__(self):
        self.stop()