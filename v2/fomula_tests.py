import numpy as np

# test = np.random.randint(100, 10000)
# print("Test value:", test)
# diagonal = np.sqrt(test**2 + test**2)

alpha = 45  # The downward tilt angle of the sensor from the horizontal plane (e.g., 45 degrees)
h = 1000  # Height of the sensor from the base level (ground)
beta = 0  # The horizontal angle between the sensor's forward direction and the measured point (left or right)
d = 100  # The distance measured by the sensor to the point

# The elevation difference is the vertical component of the measured distance, considering the tilt angle:
# Δy = h - d * sin(α) * cos(β)
delta_y = h - d * np.sin(np.deg2rad(alpha)) * np.cos(np.deg2rad(beta))
print("Elevation difference:", delta_y)

# The horizontal distance is the horizontal component of the measured distance, considering both angles:
# d_forward = d * cos(α)  # Forward component of the distance
# d_lateral = d_forward * tan(β)  # Lateral component of the distance
# x = √(d_forward² + d_lateral²) # Actual horizontal distance using Pythagorean theorem
d_forward = d * np.cos(np.deg2rad(alpha))
d_lateral = d_forward * np.tan(np.deg2rad(beta))
x = np.sqrt(d_forward**2 + d_lateral**2)
print("Horizontal distance:", x)
