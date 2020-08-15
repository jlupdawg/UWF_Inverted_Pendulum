# File: threaded_videostream_demo.py
 
import time
 
import cv2 as cv
import numpy as np
from imutils.video import VideoStream
import imutils
 
# Are we using the Pi Camera?
usingPiCamera = False
# Set initial frame size.
frameSize = (320, 240)

#Change output back to 1280x600
def gstreamer_pipeline (capture_width=1280, capture_height=720, display_width=1280, display_height=600, framerate=60, flip_method=0) :   
    return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))
 
# Initialize mutithreading the video stream.
vs = VideoStream(gstreamer_pipeline(flip_method=0), cv.CAP_GSTREAMER).start()
# Allow the camera to warm up.
time.sleep(8.0)
 
timeCheck = time.time()
while True:
	# Get the next frame.
	frame = vs.read()
	
	# If using a webcam instead of the Pi Camera,
	# we take the extra step to change frame size.
	if not usingPiCamera:
		frame = imutils.resize(frame, width=frameSize[0])
 
	# Show video stream
	cv.imshow('orig', frame)
	key = cv.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop.
	if key == ord("q"):
		break
	
	print(1/(time.time() - timeCheck))
	timeCheck = time.time()
 
# Cleanup before exit.
cv.destroyAllWindows()
vs.stop()
