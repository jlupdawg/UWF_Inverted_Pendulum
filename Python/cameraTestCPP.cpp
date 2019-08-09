// simple_gst_capture.cpp

#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>


int main()
{
     // std::cout << cv::getBuildInformation() << std::endl; 

     const char* gst = "nvarguscamerasrc  ! video/x-raw(memory:NVMM), format=(string)NV12, width=(int)640, height=(int)480, framerate=(fraction)30/1 ! \
			nvvidconv         ! video/x-raw,              format=(string)BGRx ! \
			videoconvert      ! video/x-raw,              format=(string)BGR  ! \
			appsink";

    cv::VideoCapture cap(gst);
    if(!cap.isOpened()) {
	std::cout<<"Failed to open camera."<<std::endl;
	return (-1);
    }
    
    unsigned int width  = cap.get(cv::CAP_PROP_FRAME_WIDTH); 
    unsigned int height = cap.get(cv::CAP_PROP_FRAME_HEIGHT); 
    unsigned int fps    = cap.get(cv::CAP_PROP_FPS);
    unsigned int pixels = width*height;
    std::cout <<" Frame size : "<<width<<" x "<<height<<", "<<pixels<<" Pixels "<<fps<<" FPS"<<std::endl;

    cv::namedWindow("MyCameraPreview", cv::WINDOW_AUTOSIZE);
    cv::Mat frame_in;

    while(1)
    {
    	if (!cap.read(frame_in)) {
		std::cout<<"Capture read error"<<std::endl;
		break;
	}
	
	cv::imshow("MyCameraPreview",frame_in);
	cv::waitKey(1); 
    }

    cap.release();
    return 0;
}
