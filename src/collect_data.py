import serial
import csv
import time

# Cấu hình cổng COM (Giang kiểm tra lại xem có đúng COM4 không nhé)
SERIAL_PORT = 'COM4' 
BAUD_RATE = 115200
FILE_NAME = "aikido_data.csv"

try:
    # Kết nối với ESP32
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Đợi mạch ổn định
    print(f"--- Đang bắt đầu thu thập dữ liệu từ {SERIAL_PORT} ---")
    print("Nhấn Ctrl + C để dừng và lưu file.")

    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Ghi tiêu đề cột
        writer.writerow(["Timestamp", "AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ"])

        data_row = {}
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                
                # Phân tích cú pháp định dạng >Key:Value
                if line.startswith(">"):
                    key_value = line[1:].split(":")
                    if len(key_value) == 2:
                        key, value = key_value
                        data_row[key] = value

                # Khi đã thu thập đủ 6 trục thì ghi 1 dòng vào CSV
                if len(data_row) == 6:
                    timestamp = time.strftime("%H:%M:%S", time.localtime())
                    row = [timestamp, data_row.get("AccX"), data_row.get("AccY"), 
                           data_row.get("AccZ"), data_row.get("GyroX"), 
                           data_row.get("GyroY"), data_row.get("GyroZ")]
                    writer.writerow(row)
                    print(f"Đã lưu: {row}")
                    data_row = {} # Xóa để thu thập dòng tiếp theo

except KeyboardInterrupt:
    print("\n--- Đã dừng. Dữ liệu đã được lưu vào file aikido_data.csv ---")
    ser.close()
except Exception as e:
    print(f"Lỗi: {e}")