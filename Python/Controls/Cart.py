#Command to free up camera resources: sudo systemctl restart nvargus-daemon	

#IMPORTS
import Camera
import Motors
import Controller
import time
import sys

#CONTROLLER FLAGS
#control_type = 'LQR'
control_type = 'PID'
#control_type = 'PD'
#control_type = 'COMBINED_PID'

#Controller Vectors
k = [-10.0000/1.5, -30/1.5, 822, 85.5]
pd = [3990, 0, 171]
pid = [1431, 3768, 135]

comb_pid = [[1907, 4233, 201], [1936, 406, -15]] #Theta PID vector, x PID vector
theta_weight = 0.8
x_weight = 0.2

comb_pid = [[elem * theta_weight for elem in comb_pid[0]], [elem * x_weight for elem in comb_pid[1]]]

#Set Points
SET_PT_THETA = -3.5464 * 3.141592 / 180
SET_PT_X = 0

#Global Variables
max_pwm = 85
max_theta = 15
max_x = 1

frequency = 1600 #PWM Frequency in Hz
pwm_offset = 16.67

arduino_port = '/dev/ttyUSB0'

#Booleans
display_camera_output = True
initialize_theta_set = True

class Cart():
    
    def __init__(self):
        global k, pd, pid, comb_pid, max_pwm, max_theta, max_x, frequency, pwm_offset, arduino_port, display_camera_output, initialize_theta_set
        #Cart variables
        self.max_pwm = max_pwm
        self.max_theta = max_theta
        self.max_x = max_x
        self.frequency = frequency
        self.pwm_offset = pwm_offset
        self.arduino_port = arduino_port

        #Booleans
        self.display_camera_output = display_camera_output
        self.initialize_theta_set = initialize_theta_set

        #Motor, Controller, and Camera Instance Definition
        self.motors = Motors.Motors(max_pwm = self.max_pwm, frequency=self.frequency, arduino_port=self.arduino_port)
        self.controller = Controller.Controller(max_theta = self.max_theta, max_x = self.max_x)
        self.camera = Camera.Camera(self.display_camera_output)
    
        #Controller Vectors
        self.k = [-10.0000/1.5, -29.9836/1.5, 822.2578, 85.5362]
        self.pd = pd
        self.pid = pid
        self.comb_pid = comb_pid


        self.status = 1

    def run(self):
        global SET_PT_X, SET_PT_THETA, control_type
        break_flag = False

        if self.initialize_theta_set:
            self.init_theta_set_point()
        
        while not break_flag:
            self.angle = self.camera.get_angle()
            if control_type == 'LQR' or control_type == 'COMBINED_PID':
                self.pos = self.motors.get_pos()

            if self.status:
                if control_type == 'LQR':
                    self.status, self.duty_cycle = self.controller.LQR(self.angle, self.pos, K=self.k, set_pt_theta = SET_PT_THETA, set_pt_x = SET_PT_X)
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
                self.status = 1
                self.controller.reset()
                continue
            
            if self.duty_cycle > 0:
                self.motors.forward(self.duty_cycle + self.pwm_offset)
            else:
                self.motors.backward(-self.duty_cycle + self.pwm_offset)

            break_flag = self.camera.check_for_break()

        self.camera.close()

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

                for i in range(50):
                    angles.append(self.camera.get_angle())
                    print(angles[-1])

                SET_PT_THETA = sum(angles) / len(angles)  * 3.141592 / 180
                print("Theta set point:", SET_PT_THETA)
                time.sleep(1)
                return

if __name__=="__main__":
    cart = Cart()
    cart.run()
        
