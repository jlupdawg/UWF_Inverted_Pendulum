#IMPORTS
import time

class Controller():
    def __init__(self, max_theta):
        self.curr_time = self.prev_time = 0
        self.prev_x = self.prev_theta = 0
        self.max_theta = 15
        self.theta_integral = 0

    def derivative(self, new, last, thisTime, lastTime): #Find the derivative of theta
        dt = thisTime - lastTime
        derive = (new - last)/(float(dt)/1000)
        return derive

    def LQR(self, theta, x, K=[0,0,0,0], set_pt_theta = 0, set_pt_x = 0, stat = 1, offset=0):
        if (theta > self.max_theta or theta < -self.max_theta):
            return 0,0
        theta *= 3.1415926/180
        
        self.curr_time = int(round(time.time() * 1000))  # get the current time
        theta_dot = self.derivative(theta, self.prev_theta, self.curr_time, self.prev_time)
        x_dot = self.derivative(x, self.prev_x, self.curr_time, self.prev_time)
        
        pt = self.prev_time
        self.prev_time = self.curr_time
        self.prev_theta = theta
        self.prev_x = x
        
        states = [(x-set_pt_x), x_dot, (theta-set_pt_theta), theta_dot]
        duty_cycle = sum([states[i]*K[i] for i in range(len(K))])

        for state in states:
            print(state, "\n")
        print("Time:", self.curr_time, "\n")
        print("DC: ", duty_cycle)
        print("DELTA: ", self.curr_time - pt)

        return stat, duty_cycle

    def PID(self, theta, pid=[0,0,0], set_pt_theta = 0, stat = 1, offset=0):
        [Kp, Ki, Kd] = pid
        
        if (theta > self.max_theta or theta < -self.max_theta):
            return 0,0
        theta *= 3.1415926/180
        
        self.curr_time = int(round(time.time() * 1000))  # get the current time
        theta_dot = self.derivative(theta, self.prev_theta, self.curr_time, self.prev_time)
        self.theta_integral += theta * (self.curr_time - self.prev_time) 
       
        duty_cycle = Kp * (theta - set_pt_theta) + Ki * self.theta_integral + Kd * theta_dot

        pt = self.prev_time
        self.prev_time = self.curr_time
        self.prev_theta = theta
        
        print("Time:", self.curr_time, "\n")
        print("DC: ", duty_cycle)
        print("DELTA: ", self.curr_time - pt)

        return stat, duty_cycle
