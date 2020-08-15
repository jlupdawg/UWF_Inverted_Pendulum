from threading import Thread
import cv2
import sys

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, vc):
        self.stream = vc
        self.grabbed = self.stream.grab()
        #(self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self): 
        self.t1 = Thread(target=self.get, args=())   
        self.t1.start()
        return self

    def get_stream(self):
        return self.stream

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                pass
                #self.stop()
            else:
                self.grabbed = self.stream.grab()
                #(self.grabbed, self.frame) = self.stream.read()
        raise SystemExit()

    def read(self):
        return self.stream.retrieve()
        #return (self.grabbed, self.frame)

    def get_grabbed(self):
        return self.grabbed

    def stop(self):
        print("Dedicated camera thread stopped.")
        self.stopped = True
        self.t1.join()

    def __del__(self):
        self.stop()
