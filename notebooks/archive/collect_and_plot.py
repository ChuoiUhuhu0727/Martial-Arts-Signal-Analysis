import serial
import time
import matplotlib.pyplot as plt
from collections import deque

# --- CẤU HÌNH ---
SERIAL_PORT = 'COM4' 
BAUD_RATE = 115200
WINDOW_SIZE = 100 
UPDATE_FREQ = 10 # Chỉ cập nhật đồ thị sau mỗi 10 dòng dữ liệu để tránh lag

# Khởi tạo dữ liệu
acc_x = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
acc_y = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
acc_z = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
heart_ir = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)

# Thiết lập đồ thị
plt.ion() 
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.canvas.manager.set_window_title('Aikido Smartwatch - High Precision Monitor')

line_x, = ax1.plot(range(WINDOW_SIZE), [0]*WINDOW_SIZE, label='AccX', color='r')
line_y, = ax1.plot(range(WINDOW_SIZE), [0]*WINDOW_SIZE, label='AccY', color='g')
line_z, = ax1.plot(range(WINDOW_SIZE), [0]*WINDOW_SIZE, label='AccZ', color='b')

# Cấu hình Trục 1 (IMU) - Khóa cứng để chống Clipping
ax1.set_title("Aikido Punch Dynamics (Full Scale: +/- 16g)")
ax1.set_ylim(-32768, 32767) 
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)

# Cấu hình Trục 2 (PPG) - Cho phép tự giãn để soi nhịp tim
line_hr, = ax2.plot(range(WINDOW_SIZE), [0]*WINDOW_SIZE, label='Heart IR', color='m')
ax2.set_title("Physiological Data (Heart Rate)")
ax2.grid(True, alpha=0.3)

def connect_serial():
    print(f"Đang kết nối cổng {SERIAL_PORT}...")
    while True:
        try:
            return serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        except:
            time.sleep(1)

try:
    ser = connect_serial()
    data_row = {}
    count = 0
    
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith(">"):
                    parts = line[1:].split(":")
                    if len(parts) == 2:
                        data_row[parts[0]] = parts[1]

                # Kiểm tra xem đã nhận đủ bộ 4 dữ liệu chưa
                if all(k in data_row for k in ["AccX", "AccY", "AccZ", "Heart_IR"]):
                    acc_x.append(float(data_row["AccX"]))
                    acc_y.append(float(data_row["AccY"]))
                    acc_z.append(float(data_row["AccZ"]))
                    heart_ir.append(float(data_row["Heart_IR"]))
                    
                    count += 1
                    data_row = {} # Reset để nhận bộ mới

                    # CHỈ CẬP NHẬT GIAO DIỆN KHI CẦN
                    if count % UPDATE_FREQ == 0:
                        line_x.set_ydata(list(acc_x))
                        line_y.set_ydata(list(acc_y))
                        line_z.set_ydata(list(acc_z))
                        line_hr.set_ydata(list(heart_ir))
                        
                        # CHỈ Autoscale cho đồ thị nhịp tim (ax2)
                        ax2.relim()
                        ax2.autoscale_view()

                        # KHÔNG relim/autoscale cho ax1 vì mình đã khóa +/- 32768

                        fig.canvas.flush_events()
                        plt.pause(0.001)
            except Exception as e:
                print(f"Lỗi đọc dữ liệu: {e}")

except KeyboardInterrupt:
    print("Dừng chương trình...")
finally:
    if 'ser' in locals(): ser.close()