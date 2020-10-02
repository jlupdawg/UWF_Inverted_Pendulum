#IMPORTS
import cv2 as cv
import math
import time
import VideoGet
import numpy as np

class Camera():  

    #Cropping Variables
    ymax_offset = 60
    ymin_offset = 0
    xmax_offset = -100
    xmin_offset = 100

    def __init__(self, display_camera_output = False):
        self.cam_thread = VideoGet.VideoGet(cv.VideoCapture(self.gstreamer_pipeline(flip_method=2), cv.CAP_GSTREAMER)) #connect to the camera
        #self.cam_thread = VideoGet.VideoGet(cv.VideoCapture("nvarguscamerasrc ! nvvidconv ! xvimagesink ! appsink")) #connect to the camera
        self.cam_thread.start()
        print("Camera connected!")

        #initiate font
        self.font = cv.FONT_HERSHEY_SIMPLEX
        
        frame_height = int(self.cam_thread.get_stream().get(cv.CAP_PROP_FRAME_HEIGHT)) - 150
        frame_width = int(self.cam_thread.get_stream().get(cv.CAP_PROP_FRAME_WIDTH)) - 900
        
        #instantiate images
        self.hsv_img = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        self.threshold_img1 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        self.threshold_img1a = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        self.threshold_img2 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        self.threshold_img2b = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)

        self.display_camera_output = display_camera_output

        time.sleep(3)

    def gstreamer_pipeline(self, capture_width=1280, capture_height=720, display_width=1280, display_height=600, framerate=90, flip_method=0):   
        return ('nvarguscamerasrc ! ' 
        'video/x-raw(memory:NVMM), '
        'width=(int)%d, height=(int)%d, '
        'format=(string)NV12, framerate=(fraction)%d/1 ! '
        'nvvidconv flip-method=%d ! '
        'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
        'videoconvert ! '
        'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))  #path and settings to setup the camera

    def map(self, x,in_min,in_max,out_min,out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def get_angle(self):
        while self.cam_thread.get_stream().isOpened():
            #capture the image from the cam
            ###print("Attempting to receive image from camera thread.")
            currTime = int(round(time.time() * 1000))
            ret_val, img = self.cam_thread.read()
            self.cam_thread.clear_grabbed()
            #print("8 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))

            if not ret_val:
                continue
            img = img[150:len(img), 400:len(img[1])-500]
            print("9 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))
 
            #convert the image to HSV
            self.hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

            print("10 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))
	    #self.hsv_img = cv.GaussianBlur(self.hsv_img, (0, 0), 2)
 
            #threshold the image to isolate two colors
            cv.inRange(self.hsv_img,(0,150,100),(10,255,255), self.threshold_img1) #red
            cv.inRange(self.hsv_img,(160,100,100),(179,255,255), self.threshold_img1a)   #red again
            cv.add(self.threshold_img1, self.threshold_img1a, self.threshold_img1)          #this is combining the two limits for red
	    #cv.inRange(self.hsv_img,(36,25,25),(70,255,255), self.threshold_img2)  #Green
            cv.inRange(self.hsv_img,(85,150,50),(135,255,255), self.threshold_img2)  #Blue
            print("11 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))

	    #filter out noise
            blue_kernel = np.ones((5,5), np.uint8) 
            red_kernel = np.ones((3,3), np.uint8) 

            #self.threshold_img2 = cv.erode(self.threshold_img2, blue_kernel, iterations=3) 
            #self.threshold_img2 = cv.dilate(self.threshold_img2, blue_kernel, iterations=5)
            print("12 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))

            #cv.imshow("Reds", self.threshold_img1)
            #cv.imshow("Blues", self.threshold_img2)
	   
	    #determine the moments of the two objects
            moments1=cv.moments(self.threshold_img1)
            moments2=cv.moments(self.threshold_img2)
            area1 = moments1['m00'] 
            area2 = moments2['m00'] 
            print("13 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))
             
            #initialize x and y
            x1,y1,x2,y2=(1,2,3,4)
            coord_list=[x1,y1,x2,y2]
            for x in coord_list:
                x=0
            print("14 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))
             
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
            print("15 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))

            x1=float(x1)
            y1=float(y1)
            x2=float(x2)
            y2=float(y2)

            try:
            	angle = float(math.atan((y1-y2)/(x2-x1))*180/math.pi)  #fails if the rod is perfectly vertical
            except:
                ###print("Entered angle except.")
                angle = 0
                continue
            print("16 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))

            angle = round(angle, 2)

            if angle > 0: #Make the angle show relative to the y-axis
                angle = self.map(angle, 90, 0, 0, 90)
            elif angle < 0:
                angle = self.map(angle, -90, 0, 0, -90)

            if self.display_camera_output:
                if isinstance(img, np.ndarray):
	            #this is our angle text
                    cv.putText(img,str(angle),(int(x1)+50,int(int(y2)+int(y1)/2)), self.font, 4,(255,255,255))
                    #display frames to users
                    cv.imshow("Target",img)
            print("17 ", currTime - int(round(time.time() * 1000)))

            ###print("Angle:", angle)
            return angle

    def check_for_break(self):
        c = cv.waitKey(1) % 0x100
        if c == 27 or c == 10:
            return True
        return False

    def close(self):
        print("Closing camera and terminating thread.")
        self.cam_thread.stop()
        cv.destroyAllWindows()

    def __del__(self):
        self.close()
