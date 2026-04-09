import serial
import csv
import time
import matplotlib.pyplot as plt
from collections import deque

SERIAL_PORT = 'COM4' 
BAUD_RATE = 115200
WINDOW_SIZE = 100 
MA_FILTER_SIZE = 5 

acc_x = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
acc_y = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
acc_z = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
heart_ir_filtered = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
raw_heart_buffer = deque([0]*MA_FILTER_SIZE, maxlen=MA_FILTER_SIZE)

plt.ion() 
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.canvas.manager.set_window_title('Aikido Smartwatch - Live Monitor')

line_x, = ax1.plot(range(WINDOW_SIZE), [0]*WINDOW_SIZE, label='AccX', color='r')
line_y, = ax1.plot(range(WINDOW_SIZE), [0]*WINDOW_SIZE, label='AccY', color='g')
line_z, = ax1.plot(range(WINDOW_SIZE), [0]*WINDOW_SIZE, label='AccZ', color='b')
ax1.set_title("Aikido Punch Dynamics (Accelerometer)")
ax1.legend(loc='upper right')

line_hr, = ax2.plot(range(WINDOW_SIZE), [0]*WINDOW_SIZE, label='Heart IR (Filtered)', color='m')
ax2.set_title("Physiological Data (Heart Rate)")

def connect_serial():
    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
            return ser
        except:
            time.sleep(1)

try:
    ser = connect_serial()
    data_row = {}
    count = 0
    
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith(">"):
                    parts = line[1:].split(":")
                    if len(parts) == 2:
                        data_row[parts[0]] = parts[1]

                if all(k in data_row for k in ["AccX", "AccY", "AccZ", "Heart_IR"]):
                    # DSP: Moving Average
                    val_hr = float(data_row["Heart_IR"])
                    raw_heart_buffer.append(val_hr)
                    filtered_hr = sum(raw_heart_buffer) / len(raw_heart_buffer)

                    acc_x.append(float(data_row["AccX"]))
                    acc_y.append(float(data_row["AccY"]))
                    acc_z.append(float(data_row["AccZ"]))
                    heart_ir_filtered.append(filtered_hr)

                    if count % 5 == 0:
                        line_x.set_ydata(list(acc_x))
                        line_y.set_ydata(list(acc_y))
                        line_z.set_ydata(list(acc_z))
                        line_hr.set_ydata(list(heart_ir_filtered))
                        
                        # TỰ ĐỘNG CO GIÃN CẢ 2 ĐỒ THỊ
                        ax1.relim()
                        ax1.autoscale_view()
                        ax2.relim()
                        ax2.autoscale_view()

                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        plt.pause(0.001)
                    
                    data_row = {}
                    count += 1
        except:
            ser = connect_serial()

except KeyboardInterrupt:
    ser.close()