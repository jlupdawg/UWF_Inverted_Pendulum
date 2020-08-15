#Command to free up camera resources: sudo systemctl restart nvargus-daemon	

#IMPORTS
import Camera
import Motors
import Controller
import time

#CONTROLLER FLAGS
control_type = 'LQR'
#control_type = 'PID'
#control_type = 'PD'
#control_type = 'COMBINED_PID'

#Controller Vectors
k = [-10.0000/1.5, -29.9836/1.5, 822.2578, 85.5362]
pd = [0, 0, 0]
pid = [0, 0, 0]
comb_pid = [[0, 0, 0], [0, 0, 0]]

#Set Points
SET_PT_THETA = -3.75 * 3.141592 / 180
SET_PT_X = 0

#Global Variables
max_pwm = 85
frequency = 50 #PWM Frequency in Hz
max_theta = 15
pwm_offset = 16.67
arduino_port = '/dev/ttyUSB1'

class Cart():
    
    def __init__(self):
        global k, pd, pid, comb_pid, max_pwm, frequency, max_theta, pwm_offset, arduino_port
        #Cart variables
        self.max_pwm = max_pwm
        self.frequency = frequency
        self.max_theta = max_theta
        self.pwm_offset = pwm_offset
        self.arduino_port = arduino_port

        #Motor, Controller, and Camera Instance Creation
        self.motors = Motors.Motors(max_pwm = self.max_pwm, frequency=self.frequency, arduino_port=self.arduino_port)
        self.controller = Controller.Controller(max_theta = self.max_theta)
        self.camera = Camera.Camera()
    
        #Controller Vectors
        self.k = [-10.0000/1.5, -29.9836/1.5, 822.2578, 85.5362]
        self.pd = pd
        self.pid = pid
        self.comb_pid = comb_pid

        self.status = 1

    def run(self):
        global SET_PT_X, SET_PT_THETA, control_type
        break_flag = False
        
        while not break_flag:
            self.angle = self.camera.get_angle()
            if control_type == 'LQR' or control_type == 'COMBINED_PID':
                self.pos = self.motors.get_pos()

            if self.status:
                if control_type == 'LQR':
                    self.status, self.duty_cycle = self.controller.LQR(self.angle, self.pos, K=self.k, set_pt_theta = SET_PT_THETA, set_pt_x = SET_PT_X, stat = 1)
                elif control_type == 'PID':
                    self.status, self.duty_cycle = self.controller.PID(self.angle, pid=self.pid, set_pt_theta = SET_PT_THETA, stat = 1)
                elif control_type == 'PD':
                    self.status, self.duty_cycle = self.controller.PID(self.angle, pid=self.pd, set_pt_theta = SET_PT_THETA, stat = 1)
                elif control_type == 'COMBINED_PID':
                    #self.status, self.duty_cycle = self.controller.PID(self.angle, self.pos, comb_pid=self.comb_pid, set_pt_theta = SET_PT_THETA, set_pt_x = SET_PT_X, stat = 1)
                    pass
            else:
                self.controller.PID(0)
                sleep_t = int(round(time.time() * 1000))
                while (int(round(time.time() * 1000)) - sleep_t) < 6000:
                    self.angle = self.camera.get_angle()
                    break_flag = self.camera.check_for_break()
                self.status = 1
                continue
            
            if self.duty_cycle > 0:
                self.motors.forward(self.duty_cycle + self.pwm_offset)
            else:
                self.motors.backward(-self.duty_cycle + self.pwm_offset)

            break_flag = self.camera.check_for_break()

        self.camera.close()

if __name__=="__main__":
    Cart = Cart()
    Cart.run()
        
