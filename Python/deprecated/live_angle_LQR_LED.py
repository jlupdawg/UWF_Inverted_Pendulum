import cv2 as cv
import math
import numpy as np
 
import Controls_Code_Function as Control
import time
import serial
import VideoGet

import Jetson.GPIO as GPIO

led_pin = 12
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)

f = open('output.txt', 'w')

#Command for when camera stops working: sudo systemctl restart nvargus-daemon	

#Change output back to 1280x600

def gstreamer_pipeline (capture_width=1280, capture_height=720, display_width=1280, display_height=600, framerate=60, flip_method=0) :   
    return ('nvarguscamerasrc ! ' #
    'video/x-raw(memory:NVMM), '#
    'width=(int)%d, height=(int)%d, '#
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '#
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))  #path and settings to setup the camera

#Serial port communication initialization
serial_port = serial.Serial(
	port='/dev/ttyUSB0', #CHANGE ME IF NEEDED
	baudrate=115200,
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	)
# Wait a second to let the port initialize
time.sleep(1)
serial_port.write('s'.encode())
pos = prev_pos = 0

#LQR Vector
K = [-10.0000, -29.9836, 822.2578, 85.5362]

def map(x,in_min,in_max,out_min,out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Target:

    def __init__(self):
        self.cam_thread = VideoGet.VideoGet(cv.VideoCapture(gstreamer_pipeline(flip_method=0), cv.CAP_GSTREAMER)) #connect to the camera

        #self.cam_thread = VideoGet.VideoGet(cv.VideoCapture("nvarguscamerasrc ! nvvidconv ! xvimagesink ! appsink")) #connect to the camera

        self.cam_thread.start()
        print("Camera connected!")

    def run(self):
        #initiate font
        font = cv.FONT_HERSHEY_SIMPLEX
        
        frame_height = int(self.cam_thread.get_stream().get(cv.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(self.cam_thread.get_stream().get(cv.CAP_PROP_FRAME_WIDTH))
        
        #instantiate images
        hsv_img = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        threshold_img1 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        threshold_img1a = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        threshold_img2 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        threshold_img2b = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        i=0
 	
	##################################################### Change these values #############################################

        status = 1
        lastTime = int(round(time.time() * 1000))
        startTime = lastTime
        setPoint = 0
        highAngle = 30
        oldAngle = 0
        Kp = 11   ##11   11
        Kd = 1.25 ##.2   1.25
        derivative = 0
	
	######################################################################################################################	

        time.sleep(3)

        while self.cam_thread.get_stream().isOpened():
            #capture the image from the cam
            if self.cam_thread.get_grabbed():
            	ret_val, img = self.cam_thread.read();
            else:
                continue
 
            #convert the image to HSV
            hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	    #hsv_img = cv.GaussianBlur(hsv_img, (0, 0), 2)
 
            #threshold the image to isolate two colors
            cv.inRange(hsv_img,(0,10,10),(10,255,255),threshold_img1) #red
            cv.inRange(hsv_img,(160,100,100),(179,255,255),threshold_img1a)   #red again
            cv.add(threshold_img1,threshold_img1a,threshold_img1)          #this is combining the two limits for red
	    #cv.inRange(hsv_img,(36,25,25),(70,255,255),threshold_img2)  #Green
            cv.inRange(hsv_img,(85,60,50),(135,255,255),threshold_img2)  #blue
	    
	   	
            
	    #filter out noise
            blue_kernel = np.ones((5,5), np.uint8) 
            red_kernel = np.ones((3,3), np.uint8) 
            threshold_img2 = cv.erode(threshold_img2, blue_kernel, iterations=3) 
            threshold_img2 = cv.dilate(threshold_img2, blue_kernel, iterations=5)
            threshold_img1 = cv.erode(threshold_img1, red_kernel, iterations=5) 
            threshold_img1 = cv.dilate(threshold_img1, red_kernel, iterations=5) 

            #cv.imshow("Reds",threshold_img1)
            #cv.imshow("Blues",threshold_img2)
	   
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
             
            #Ignore if the image was over-filtered (the area is too small)
            if (area1 >10000):
                #x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                x1=int(moments1['m10']/area1)
                y1=int(moments1['m01']/area1)
 
                #draw circle
                cv.circle(img,(x1,y1),50,(0,0,255),2)
 
            if (area2 >10000):
                #x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                x2=int(moments2['m10']/area2)
                y2=int(moments2['m01']/area2)
 
                #draw circle
                cv.circle(img,(x2,y2),50,(255,0,0),2)
 
		#draw line measure angle
                cv.line(img,(x1,y1),(x2,y2),(0,255,0),4,cv.LINE_AA)

            x1=float(x1)
            y1=float(y1)
            x2=float(x2)
            y2=float(y2)

            try:
            	angle = float(math.atan((y1-y2)/(x2-x1))*180/math.pi)  #fails if the rod is perfectly vertical
            except:
                print("Entered angle except.")
                angle = 0
                continue

            angle = round(angle, 2)

            if angle > 0: #Make the angle show relative to the y-axis
                angle = map(angle, 90, 0, 0, 90)
            elif angle < 0:
                angle = map(angle, -90, 0, 0, -90)

            if angle<0:
                GPIO.output(led_pin, GPIO.HIGH)
            else:
                GPIO.output(led_pin, GPIO.LOW)

            #Read position from arduino
            serial_port.write('r'.encode())
            while serial_port.inWaiting() == 0:
                print("Waiting on serial.")
                pass
            pos = int(serial_port.readline().decode('utf-8')) / 1000 * 2 * 3.141592 * 0.05
            print("Read pos: ", pos)

            
            #Make call to controls
            
            if(True or status == 1):
		#print ("Last Time = " + str(lastTime))
                #status, oldAngle , lastTime, derivative, PD = Control.PID(angle, Kp, Kd, highAngle, setPoint, lastTime, oldAngle, status)
		
                status, duty_cycle = Control.LQR(angle, pos, K, set_pt_theta = 0, set_pt_x = 0, stat = 1)
                #print("Angle = " + str(angle))
		#print("Derivative = " + str(derivative))
                #print("Time = " + str(lastTime))
                print("Loop time =", int(round(time.time() * 1000)) - lastTime)
                lastTime = int(round(time.time() * 1000))
                f.write("%i %2.2f %2.1f \n" % ((lastTime-startTime), angle, duty_cycle))
            else:
                Control.LQR(0,0)
                time.sleep(6)
                t.run()	#Runs the code again to check if the rod is back in place
                break
            if isinstance(img, np.ndarray):
	        #this is our angle text
                cv.putText(img,str(angle),(int(x1)+50,int(int(y2)+int(y1)/2)),font, 4,(255,255,255))
                #display frames to users
                cv.imshow("Target",img)

            # Listen for ESC or ENTER key
            c = cv.waitKey(7) % 0x100
            if c == 27 or c == 10:
                self.cam_thread.stop()
                break
        cv.destroyAllWindows()
        f.close()
             
if __name__=="__main__":
    t = Target()
    t.run()        
