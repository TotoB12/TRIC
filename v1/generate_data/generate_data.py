import datetime
import random

num_lines = int(input("Enter the number of lines to generate: "))

current_timestamp = datetime.datetime(2023, 5, 18, 22, 0, 0, 60000)

with open("data\data.txt", "w") as f:
    f.write("2023-05-18_22:00:00.60, 0.0, 0.0, 38.0\n")

    for _ in range(1, num_lines):
        current_timestamp += datetime.timedelta(seconds=1)
        timestamp = current_timestamp.strftime("%Y-%m-%d_%H:%M:%S.%f")[:-3]
        xdis = random.uniform(-0.02, 0.02)
        ydis = random.uniform(-0.02, 0.02)
        zdis = random.randint(35, 40)
        f.write(f"{timestamp}, {xdis}, {ydis}, {zdis}\n")
