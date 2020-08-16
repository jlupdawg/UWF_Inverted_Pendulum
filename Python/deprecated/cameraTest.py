# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a 
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import VideoGet
import numpy

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps 
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

def gstreamer_pipeline (capture_width=640, capture_height=360, display_width=1280, display_height=720, framerate=30, flip_method=0) :   
    return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))

def show_camera():
    global get_thread
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    #print gstreamer_pipeline(flip_method=0)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    get_thread = VideoGet.VideoGet(cap)
    get_thread.start()

    if get_thread.get_stream().isOpened():
        window_handle = cv2.namedWindow('CSI Camera', cv2.WINDOW_AUTOSIZE)
        # Window 
        while cv2.getWindowProperty('CSI Camera',0) >= 0:
            if get_thread.get_grabbed():
            	ret_val, img = get_thread.read();
            else:
                continue
            if isinstance(img, numpy.ndarray):
                cv2.imshow('CSI Camera',img)
	    # This also acts as 
            keyCode = cv2.waitKey(30) & 0xff
            # Stop the program on the ESC key
            if keyCode == 27:
               get_thread.stop()
               break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print('Unable to open camera')


if __name__ == '__main__':
    global get_thread
    show_camera()
    get_thread.stop()