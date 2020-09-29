#IMPORTS
import time
import numpy as np
from array import *


class Filtering():
    def __init__(self):
        self.num_measurements = 3
        self.degrees = 2
        self.time_list =[0]*num_measurements
        self.angle_list = [0]*num_measurements
        self.time_array = np.ones(num_measurements,degrees)

    def update_lists(self, new_time, new_angle):
        np.roll(self.time_list,1)
        np.roll(self.angle_list,1)

        self.time_list[-1] = new_time
        self.angle_list[-1] = new_angle

    def update_arrays(self):
        for i in range(len(self.time_array)):
            for j in range(len(self.time_array[i])):
                self.time_array[i][j] = time_list[j]^(i-1)
    
    def get_coeffs(self):
        self.update_arrays()
        return np.linalg.lstsq(self.time_array, self.angle_list)
    
    def get_derivedcoeffs(self):
        x = self.get_coeffs()
        y = len(x)
        x.pop()
        j = 0
        for i in x:
            x[j] = i*y
            j = j+1
        return x
            
        
    
        
