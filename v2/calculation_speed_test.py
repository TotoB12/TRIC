import timeit
import numpy as np

alpha = 45
h = 1000
beta = 0
d = 100

def calculation():
    delta_y = h - d * np.sin(np.deg2rad(alpha)) * np.cos(np.deg2rad(beta))
    d_forward = d * np.cos(np.deg2rad(alpha))
    d_lateral = d_forward * np.tan(np.deg2rad(beta))
    x = np.sqrt(d_forward**2 + d_lateral**2)
    # print("Elevation difference:", delta_y)
    # print("Horizontal distance:", x)
    pass

execution_time = timeit.timeit(calculation, number=10000)
print(f"Execution time for 10000 calculations: {execution_time} seconds")
