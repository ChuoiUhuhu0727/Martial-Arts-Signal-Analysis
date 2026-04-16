import serial
import csv
import time
import os

# --- Cấu hình ---
SERIAL_PORT = 'COM4' 
BAUD_RATE = 115200
SAVE_DIR = r"C:\Users\Admin\Downloads\draft_one_signal_final_project\src"
FILENAME = os.path.join(SAVE_DIR, f"aikido_data_{int(time.time())}.csv")

def collect():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        print(f"--- ĐANG THU THẬP DỮ LIỆU ---")
        print(f"File: {FILENAME}")
        
        with open(FILENAME, mode='w', newline='') as f:
            fieldnames = ["Timestamp", "AccX", "AccY", "AccZ", "Heart_IR"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # Khởi tạo buffer với giá trị None để dễ kiểm tra trạng thái
            current_data = {"AccX": None, "AccY": None, "AccZ": None, "Heart_IR": None}
            start_time = time.time()
            
            # Biến đếm để tránh spam cảnh báo quá nhiều
            error_counter = 0

            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line.startswith(">"):
                        parts = line[1:].split(":")
                        if len(parts) == 2:
                            key, val = parts[0], parts[1]
                            try:
                                current_data[key] = int(val)
                            except ValueError:
                                continue

                            # TRIGGER: AccZ là điểm chốt dòng (Master Trigger)
                            if key == "AccZ":
                                current_data["Timestamp"] = time.time() - start_time
                                
                                # --- LOGIC CHẨN ĐOÁN (DIAGNOSTICS) ---
                                status_msg = "OK"
                                ppg_val = current_data.get("Heart_IR")

                                if ppg_val is None:
                                    status_msg = "⚠️ MISSING PPG (Check ESP32 Code)"
                                elif ppg_val == 0:
                                    status_msg = "❌ PPG = 0 (Check Sensor/Wiring)"
                                
                                # Ghi vào CSV (vẫn ghi để giữ data IMU)
                                # Nếu PPG trống, điền tạm số 0 để file CSV không lỗi cấu trúc
                                row_to_write = {k: (v if v is not None else 0) for k, v in current_data.items()}
                                writer.writerow(row_to_write)
                                
                                # In thông báo trạng thái real-time
                                print(f"T: {current_data['Timestamp']:.1f}s | Z: {val} | IR: {ppg_val} | Status: {status_msg}      ", end='\r')
                                
                                # Reset buffer (giữ lại None để vòng sau kiểm tra tiếp)
                                current_data = {"AccX": None, "AccY": None, "AccZ": None, "Heart_IR": None}

    except KeyboardInterrupt:
        print(f"\n--- ĐÃ DỪNG THU THẬP ---")
        print(f"Dữ liệu lưu tại: {FILENAME}")
    finally:
        if 'ser' in locals(): ser.close()

if __name__ == "__main__":
    collect()