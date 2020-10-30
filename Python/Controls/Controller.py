#IMPORTS
import time

class Controller():
    def __init__(self, FILTER_SIZE=3, max_theta=15, max_x=1):
        self.prev_x = self.prev_theta = 0
        self.max_theta = max_theta
        self.max_x = max_x
        self.f = open("ControllerOutput.txt","w")
        self.reset()
        self.FILTER_SIZE = FILTER_SIZE
        self.filter = []
        self.theta_queue = [0, 0, 0]
        self.time_queue = [0, 0, 0]
        print("FILTER_SIZE:", FILTER_SIZE)

    def derivative(self, new, last, thisTime, lastTime):
        dt = thisTime - lastTime
        if dt != 0:
            derive = (new - last)/(float(dt)/1000)
            return derive
        else: return 0

    def LQR(self, theta, x, K=[0,0,0,0], set_pt_theta = 0, set_pt_x = 0):
        if (theta > self.max_theta or theta < -self.max_theta):
            return 0,0
        theta *= 3.1415926/180

        #Moving average filter for derivative smoothing
        prev_filter = self.filter.copy()
        if len(self.filter) == self.FILTER_SIZE:
            self.filter.pop()
        self.filter = [theta] + self.filter

        ###print(self.filter)
        ###print(prev_filter)

        self.curr_time = int(round(time.time() * 1000))  # get the current time

        prev_theta_avg = sum(prev_filter) / len(prev_filter) if len(prev_filter) else 0
        theta_avg = sum(self.filter) / len(self.filter)
        '''self.theta_queue.pop()
        self.theta_queue = [theta] + self.theta_queue
        self.time_queue.pop()
        self.time_queue = [self.curr_time] + self.time_queue
        print(self.theta_queue)
        print(self.time_queue)'''

        #theta_dot = (3*self.theta_queue[0] - 4*self.theta_queue[1] + self.theta_queue[2]) / (self.time_queue[0] - self.time_queue[2]) * 1000
        
        theta_dot = self.derivative(theta_avg, prev_theta_avg, self.curr_time, self.prev_time)
        #theta_dot = self.derivative(theta, self.prev_theta, self.curr_time, self.prev_time)
        x_dot = self.derivative(x, self.prev_x, self.curr_time, self.prev_time)
        
        pt = self.prev_time
        self.prev_time = self.curr_time
        self.prev_theta = theta
        self.prev_x = x
        
        states = [(x-set_pt_x), x_dot, (theta-set_pt_theta), theta_dot]
        duty_cycle = sum([states[i]*K[i] for i in range(len(K))])

        write_states = [set_pt_theta, self.curr_time, duty_cycle]
        write_states += states
        self.toFile(write_states) 

        '''for state in states:
            print(state, "\n")
        print("Time:", self.curr_time, "\n")
        print("DC: ", duty_cycle)
        print("DELTA: ", self.curr_time - pt)'''

        return 1, duty_cycle

    def PID(self, theta, pid=[0,0,0], set_pt_theta = 0, stat = 1):
        [Kp, Ki, Kd] = pid
        
        if (theta > self.max_theta or theta < -self.max_theta):
            return 0,0
        theta *= 3.1415926/180
        
        self.curr_time = int(round(time.time() * 1000))  # get the current time
        theta_dot = self.derivative(theta, self.prev_theta, self.curr_time, self.prev_time)
        self.theta_integral += theta * (self.curr_time - self.prev_time) / 1000
       
        duty_cycle = Kp * (theta - set_pt_theta) + Ki * self.theta_integral + Kd * theta_dot

        pt = self.prev_time
        self.prev_time = self.curr_time
        self.prev_theta = theta
        
        print("Time:", self.curr_time, "\n")
        print("DC: ", duty_cycle)
        print("DELTA: ", self.curr_time - pt)

        write_states = [self.curr_time, duty_cycle, theta - set_pt_theta, self.theta_integral, theta_dot]
        self.toFile(write_states) 

        return 1, duty_cycle

    def PID_pos(self, x, pid=[0,0,0], set_pt_x = 0):
        [Kp, Ki, Kd] = pid

        if (x > self.max_x or x < -self.max_x):
            return 0,0
        
        self.curr_time = int(round(time.time() * 1000))  # get the current time
        x_dot = self.derivative(x, self.prev_x, self.curr_time, self.prev_time)
        self.x_integral += x * (self.curr_time - self.prev_time) / 1000
       
        duty_cycle = Kp * (x - set_pt_x) + Ki * self.x_integral + Kd * x_dot

        pt = self.prev_time
        self.prev_time = self.curr_time
        self.prev_x = x
        
        print("Time:", self.curr_time, "\n")
        print("DC: ", duty_cycle)
        print("DELTA: ", self.curr_time - pt)

        return 1, duty_cycle

    def comb_PID(self, theta, x, comb_pid = [[0,0,0],[0,0,0]], set_pt_theta = 0, set_pt_x = 0):
        theta_stat, theta_dc = self.PID(theta, comb_pid[0], set_pt_theta)
        x_stat, x_dc = self.PID_pos(x, comb_pid[1], set_pt_x)

        return min(theta_stat, x_stat), theta_dc + x_dc

    def reset(self):
        self.curr_time = self.prev_time = int(round(time.time() * 1000))
        self.theta_integral = 0
        self.x_integral = 0

        self.f.write("---------------------------------------\n")
        self.f.write("Time Duty_cycle X X_dot Theta Theta_dot\n")

    def toFile(self, write_states):
        for x in write_states:
            self.f.write(str(x) + " ")
        self.f.write("\n")

    def close(self):
        self.f.close()
