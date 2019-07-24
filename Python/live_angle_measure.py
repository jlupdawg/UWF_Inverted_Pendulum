import cv2 as cv
import math
import numpy as np
 
import Controls_Code_Function as Control
import time

def gstreamer_pipeline (capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=60, flip_method=0) :   
    return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))

def map(x,in_min,in_max,out_min,out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Target:

    def __init__(self):
        self.capture = cv.VideoCapture(gstreamer_pipeline(flip_method=0), cv.CAP_GSTREAMER)

    def run(self):
        #initiate font
        font = cv.FONT_HERSHEY_SIMPLEX
        
        frame_height = int(self.capture.get(cv.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(self.capture.get(cv.CAP_PROP_FRAME_WIDTH))
        
        #instantiate images
        hsv_img = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        threshold_img1 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        threshold_img1a = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        threshold_img2 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
 	threshold_img2b = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        i=0
 
	status = 1
    	lastTime = int(round(time.time() * 1000))
	setPoint = 0
    	highAngle = 30
   	oldAngle = 0
    	Kp = 50
    	Kd = 10
	derivative = 0

	time.sleep(3)

        while True:

            #capture the image from the cam
            ret, img=self.capture.read()
 
            #convert the image to HSV
            hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
 
            #threshold the image to isolate two colors
            cv.inRange(hsv_img,(165,145,100),(250,210,160),threshold_img1) #red
            cv.inRange(hsv_img,(0,145,100),(10,210,160),threshold_img1a)   #red again
            cv.add(threshold_img1,threshold_img1a,threshold_img1)          #this is combining the two limits for red
	    #cv.inRange(hsv_img,(36,25,25),(70,255,255),threshold_img2)  #Green
            cv.inRange(hsv_img,(105,180,40),(120,260,100),threshold_img2)  #blue
	    cv.inRange(hsv_img,(0,180,40),(42,260,100),threshold_img2b)  #blue
            cv.add(threshold_img2,threshold_img2b,threshold_img2)          #this is combining the two limits for red
 
            #determine the moments of the two objects
            moments1=cv.moments(threshold_img1)
            moments2=cv.moments(threshold_img2)
            area1 = moments1['m00'] 
            area2 = moments2['m00'] 
             
            #initialize x and y
            x1,y1,x2,y2=(1,2,3,4)
            coord_list=[x1,y1,x2,y2]
            for x in coord_list:
                x=0
             
            #there can be noise in the video so ignore objects with small areas
            if (area1 >200000):
                #x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                x1=int(moments1['m10']/area1)
                y1=int(moments1['m01']/area1)
 
                #draw circle
                cv.circle(img,(x1,y1),2,(0,0,255),20)
 
 
            if (area2 >100000):
                #x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                x2=int(moments2['m10']/area2)
                y2=int(moments2['m01']/area2)
 
                #draw circle
                cv.circle(img,(x2,y2),2,(255,0,0),20)
 
		#draw line measure angle
                cv.line(img,(x1,y1),(x2,y2),(0,255,0),4,cv.LINE_AA)
            x1=float(x1)
            y1=float(y1)
            x2=float(x2)
            y2=float(y2)

	    try:
            	angle = float(math.atan((y1-y2)/(x2-x1))*180/math.pi)
	    except:
		angle = 0
		continue

	    angle = round(angle, 2)

	    if angle > 0:
		angle = map(angle, 90, 0, 0, 90)
	    elif angle < 0:
		angle = map(angle, -90, 0, 0, -90)

	    #Make call to controls
	    if(status == 1):
		#print ("Last Time = " + str(lastTime))
        	status, oldAngle , lastTime, derivative = Control.PID(angle, Kp, Kd, highAngle, setPoint, lastTime, oldAngle, status)	
	        print("Angle = " + str(angle))
		print("Derivative = " + str(derivative))
		print("Time Delay = " + str(lastTime))
    	    else:
        	Control.PID(0)
     		break
	
	    #this is our angle text
            cv.putText(img,str(angle),(int(x1)+50,(int(y2)+int(y1))/2),font, 4,(255,255,255))

            #display frames to users
            cv.imshow("Target",img)

            # Listen for ESC or ENTER key
            c = cv.waitKey(7) % 0x100
            if c == 27 or c == 10:
                break
        cv.destroyAllWindows()
             
if __name__=="__main__":
    t = Target()
    t.run()        
