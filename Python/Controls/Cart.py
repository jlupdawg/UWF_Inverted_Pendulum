#Command to free up camera resources: sudo systemctl restart nvargus-daemon	

#IMPORTS
import Camera
import Motors
import Controller
import time
import sys

#CONTROLLER FLAGS
from SerialThread import SerialThread

control_type = 'LQR'
#control_type = 'PID'
#control_type = 'PD'
#control_type = 'COMBINED_PID'

#Controller Vectors
#k= [-10, -30.3842, 845.1755, 62.9270]
#k= [-5, -15, 1500, 63] #This works pretty well
k= [-5, -15, 1600, 75]
#k= [-10, -30.3842, 900.1755, 135] #May work when battery fully charged
#k= [-10, -30.3842, 930.1755, 100]
#k = [-10, -30.3842, 1000, 85] #Too much oscillation

pd = [3990, 0, 171]
pid = [1431, 5000, 370]#3768, 135]
#pid = [1350, 4000, 0]

comb_pid = [[1907, 4233, 201], [1936, 406, -15]] #Theta PID vector, x PID vector
theta_weight = 0.8
x_weight = 0.2

comb_pid = [[elem * theta_weight for elem in comb_pid[0]], [elem * x_weight for elem in comb_pid[1]]]

#Set Points
SET_PT_THETA = 180 * 3.141592 / 180
SET_PT_X = 0

#Global Variables
max_pwm = 95
max_theta = 15
max_x = 1

#Theta derivative filtering
FILTER_SIZE = 1 #Size of running average of theta

frequency = 1600 #PWM Frequency in Hz
pwm_offset = 16.67

arduino_port = '/dev/arduino_top'

#Booleans
display_camera_output = True
initialize_theta_set = True

class Cart():
    
    def __init__(self):
        global k, pd, pid, comb_pid, max_pwm, max_theta, max_x, frequency, pwm_offset, arduino_port, display_camera_output, initialize_theta_set, FITER_SIZE
        #Cart variables
        self.max_pwm = max_pwm
        self.max_theta = max_theta
        self.max_x = max_x
        self.frequency = frequency
        self.pwm_offset = pwm_offset
        self.arduino_port = arduino_port

        self.f = open("timeAnalysis" + str(time.time()) + ".txt", "w")

        #Booleans
        self.display_camera_output = display_camera_output
        self.initialize_theta_set = initialize_theta_set

        #Motor, Controller, and Camera Instance Definition
        self.motors = Motors.Motors(max_pwm = self.max_pwm, frequency=self.frequency, arduino_port=self.arduino_port)
        self.encoder2 = SerialThread()
        self.encoder2.start()
        self.encoder2pos = 0
        self.controller = Controller.Controller(FILTER_SIZE, max_theta = self.max_theta, max_x = self.max_x)
        self.camera = Camera.Camera(self.display_camera_output)
    
        #Controller Vectors
        self.k = k
        self.pd = pd
        self.pid = pid
        self.comb_pid = comb_pid

        self.filter_time = 0
        self.sensor_time = 0


        self.status = 1

    def run(self):
        global SET_PT_X, SET_PT_THETA, control_type
        #print("Inside run")
        break_flag = False

        if self.initialize_theta_set:
            self.init_theta_set_point()
        
        while not break_flag:
            currTime = int(round(time.time() * 1000))
            #self.angle, self.filter_time, self.sensor_time = self.camera.get_angle()
            self.angle = self.camera.get_angle()
            # self.f.write(str(int(round(time.time() * 1000)) - currTime) + "\n")
            self.encoder2pos = self.encoder2.get_pos()
            print("Adjusted angle: ", self.angle - SET_PT_THETA * 180 / 3.141592)
            #print("1: ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))

            if control_type == 'LQR' or control_type == 'COMBINED_PID':
                self.pos = self.motors.get_pos()
            print(str(self.pos))
            #print("2: ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))

            #self.f.write(str(time.time() * 1000) + " " + str(self.angle - SET_PT_THETA * 180 / 3.141592) + " " + str(self.pos) + "\n")
            #self.f.write(str(self.filter_time) + " " + str(self.sensor_time) + "\n")

            if self.status:
                #print(self.status, " is status.")
                if control_type == 'LQR':
                    self.status, self.duty_cycle = self.controller.LQR(self.angle, self.pos, self.encoder2pos, K=self.k, set_pt_theta = SET_PT_THETA, set_pt_x = 0)
                elif control_type == 'PID':
                    self.status, self.duty_cycle = self.controller.PID(self.angle, pid=self.pid, set_pt_theta = SET_PT_THETA)
                elif control_type == 'PD':
                    self.status, self.duty_cycle = self.controller.PID(self.angle, pid=self.pd, set_pt_theta = SET_PT_THETA)
                elif control_type == 'COMBINED_PID':
                    self.status, self.duty_cycle = self.controller.comb_PID(self.angle, self.pos, comb_pid=self.comb_pid, set_pt_theta = SET_PT_THETA, set_pt_x = SET_PT_X)
            else:
                self.motors.forward(0)
                sleep_t = int(round(time.time() * 1000))
                while (int(round(time.time() * 1000)) - sleep_t) < 6000:
                    self.angle = self.camera.get_angle()
                    break_flag = self.camera.check_for_break()
                    if break_flag: break
                self.status = 1
                self.controller.reset()
                continue
            
            if self.duty_cycle > 0:
                self.motors.forward(self.duty_cycle + self.pwm_offset)
            else:
                self.motors.backward(-self.duty_cycle - self.pwm_offset)

            #print("4: ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))
            if display_camera_output: break_flag = self.camera.check_for_break()
            #print("5 ", currTime - int(round(time.time() * 1000)))
            currTime = int(round(time.time() * 1000))

        print("Closing Down")        
        self.camera.close()
        self.controller.close()
        self.motors.close()

    def init_theta_set_point(self):
        global SET_PT_THETA
        init_inp = "None"

        while init_inp not in ["skip", "begin"] and type(init_inp) != float:
            init_inp = input("Initializing theta set point. Please type 'skip', 'begin', or a float value representing the desired set point.\n")

            if init_inp == 'skip':
                return
            elif type(init_inp) == float:
                SET_PT_THETA = init_inp
                return
            elif init_inp == 'begin':
                print("Beginning measurement.")
                time.sleep(0.25)
                angles = []

                for i in range(100):
                    angles.append(self.camera.get_angle())
                    print(angles[-1])

                SET_PT_THETA = sum(angles) / len(angles) * 3.141592 / 180
                print("Theta set point:", SET_PT_THETA)
                time.sleep(1)
                return

if __name__=="__main__":
    cart = Cart()
    cart.run()
    cart.f.close()
        
