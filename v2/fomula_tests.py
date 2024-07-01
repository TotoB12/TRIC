import numpy as np

# - α (alpha): The downward tilt angle of the sensor from the horizontal plane (e.g., 45 degrees)
# - h: Height of the sensor from the base level (ground)
# - β (beta): The horizontal angle between the sensor's forward direction and the measured point (left or right)
# - d: The distance measured by the sensor to the point

alpha = 45
h = 1000
beta = 0
d = 1236

# The elevation difference is the vertical component of the measured distance, considering the tilt angle:
# Δy = h - d * sin(α) * cos(β)
delta_y = h - d * np.sin(np.deg2rad(alpha)) * np.cos(np.deg2rad(beta))
print(delta_y)

# The horizontal distance is the horizontal component of the measured distance, considering both angles:
# x = d * cos(α) * cos(β)
x = d * np.cos(np.deg2rad(alpha)) * np.cos(np.deg2rad(beta))
print(x)
