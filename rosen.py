import numpy as np
import pandas as pd 
import random


samples_number = 10000

inputs_number = 2

distribution = random.uniform(-1, 1)

inputs = np.random.uniform(-1.0, 1.0, size = (samples_number, inputs_number))

rosenbrock = []

for j in range (samples_number):
    
    r = 0
    
    for i in range(inputs_number-1):
        
        r += (1.0 - inputs[j][i])*(1.0 - inputs[j][i])+100.0*((inputs[j][i+1]-inputs[j][i]*inputs[j][i])*(inputs[j][i+1]-inputs[j][i]*inputs[j][i]))
        
    rosenbrock.append(r)


print(rosenbrock)