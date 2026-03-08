import serial
import csv
import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

PORT = "/dev/cu.wchusbserial56440196321"   # skift til din port
BAUD = 115200
CSV_FILE = "imu_walk1.csv"
MAX_POINTS = 1000

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

csv_file = open(CSV_FILE, "w", newline="")
writer = csv.writer(csv_file)
writer.writerow(["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"])

x_vals = deque(maxlen=MAX_POINTS)
acc_x_vals = deque(maxlen=MAX_POINTS)
acc_y_vals = deque(maxlen=MAX_POINTS)
acc_z_vals = deque(maxlen=MAX_POINTS)
gyro_x_vals = deque(maxlen=MAX_POINTS)
gyro_y_vals = deque(maxlen=MAX_POINTS)
gyro_z_vals = deque(maxlen=MAX_POINTS)

counter = 0

fig, ax = plt.subplots()
line1, = ax.plot([], [], label="acc_x")
line2, = ax.plot([], [], label="acc_y")
line3, = ax.plot([], [], label="acc_z")
line4, = ax.plot([], [], label="gyro_x")
line5, = ax.plot([], [], label="gyro_y")
line6, = ax.plot([], [], label="gyro_z")

ax.set_title("ESP32 IMU live data")
ax.set_xlabel("Sample")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True)

def update(frame):
    global counter

    while ser.in_waiting:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) != 6:
            continue

        try:
            acc_x = float(parts[0])
            acc_y = float(parts[1])
            acc_z = float(parts[2])
            gyro_x = float(parts[3])
            gyro_y = float(parts[4])
            gyro_z = float(parts[5])
        except ValueError:
            continue

        writer.writerow([acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z])
        csv_file.flush()

        x_vals.append(counter)
        acc_x_vals.append(acc_x)
        acc_y_vals.append(acc_y)
        acc_z_vals.append(acc_z)
        gyro_x_vals.append(gyro_x)
        gyro_y_vals.append(gyro_y)
        gyro_z_vals.append(gyro_z)
        counter += 1

    if len(x_vals) > 0:
        line1.set_data(x_vals, acc_x_vals)
        line2.set_data(x_vals, acc_y_vals)
        line3.set_data(x_vals, acc_z_vals)
        line4.set_data(x_vals, gyro_x_vals)
        line5.set_data(x_vals, gyro_y_vals)
        line6.set_data(x_vals, gyro_z_vals)

        ax.set_xlim(min(x_vals), max(x_vals) if max(x_vals) > 0 else 1)

        all_vals = (
            list(acc_x_vals) + list(acc_y_vals) + list(acc_z_vals) +
            list(gyro_x_vals) + list(gyro_y_vals) + list(gyro_z_vals)
        )
        y_min = min(all_vals) - 0.5
        y_max = max(all_vals) + 0.5
        ax.set_ylim(y_min, y_max)

    return line1, line2, line3, line4, line5, line6

ani = FuncAnimation(fig, update, interval=50, blit=False)

try:
    plt.show()
finally:
    ser.close()
    csv_file.close()