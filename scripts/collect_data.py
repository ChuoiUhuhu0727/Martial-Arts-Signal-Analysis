import serial
import csv
import time
import os

# --- CONFIGURATION ---
SERIAL_PORT = 'COM4' # Nhắc Duy (Member 3) đổi đúng cổng COM trên máy bạn ấy nhé
BAUD_RATE = 115200

# THIẾT LẬP ĐƯỜNG DẪN TƯƠNG ĐỐI (RELATIVE PATHS)
# Tự động tìm vị trí của folder scripts/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Nhảy ra ngoài project root rồi đi vào folder data/raw/
SAVE_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "data", "raw"))

# Tạo folder nếu chưa tồn tại để tránh lỗi "Folder not found"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# --- PROTOCOLS BASED ON "TÂM TƯ SIGNAL" (GIỮ NGUYÊN) ---
PROTOCOLS = {
    "LIGHT":   [{"n": "REST", "d": 20, "p": 0}, {"n": "PUNCH", "d": 20, "p": 1}, {"n": "RECOVERY", "d": 40, "p": 2}],
    "MEDIUM":  [{"n": "REST", "d": 15, "p": 0}, {"n": "PUNCH", "d": 30, "p": 1}, {"n": "RECOVERY", "d": 45, "p": 2}],
    "INTENSE": [{"n": "REST", "d": 15, "p": 0}, {"n": "PUNCH", "d": 45, "p": 1}, {"n": "RECOVERY", "d": 60, "p": 2}],
    "FATIGUE": [{"n": "REST", "d": 15, "p": 0}, {"n": "PUNCH", "d": 45, "p": 1}, {"n": "RECOVERY", "d": 60, "p": 2}],
    "RANDOM":  [{"n": "RANDOM MOVEMENT", "d": 60, "p": 0}],
    "STILL":   [{"n": "STILL MOVEMENT", "d": 60, "p": 0}]
}

# --- DETAILED INSTRUCTIONS (GIỮ NGUYÊN) ---
INSTRUCTIONS = {
    "CLEAN": "Perform standard, crisp martial arts punches.",
    "NOISY": "Add wrist rotations or open/close fist while punching to create noise.",
    "VARIATION": "Vary speeds (fast/slow) and strength within this session.",
    "FATIGUE": "Start strong, then gradually slow down as you get tired.",
    "RANDOM": "Perform natural arm movements (scratching head, fixing clothes).",
    "STILL": "Stand completely still. Do not move the sensor arm."
}

def collect():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("\n" + "="*55)
        print("   AIKIDO DATA COLLECTION ASSISTANT (PORTABLE VERSION)")
        print("="*55)
        
        # 1. Input Metadata
        session = input("Session Type (LIGHT/MEDIUM/INTENSE/FATIGUE/RANDOM/STILL): ").upper()
        prop = input("Property (CLEAN/NOISY/VARIATION): ").upper() if session not in ["RANDOM", "STILL"] else "NA"
        trial = input("Trial Number (e.g., 01, 02): ")
        
        # Đặt tên file tự động kèm timestamp
        filename = f"{session}_{prop}_{trial}_{int(time.time())}.csv"
        filepath = os.path.join(SAVE_DIR, filename)
        phases = PROTOCOLS.get(session, PROTOCOLS["STILL"])

        print(f"\n[READY] Target Folder: {SAVE_DIR}")
        print(f"[READY] Target File: {filename}")
        guide_key = session if session in ["RANDOM", "STILL"] else prop
        print(f"[GUIDE] {INSTRUCTIONS.get(guide_key, 'Follow standard protocol.')}")
        input("\n>>> Press ENTER khi cậu đã sẵn sàng vào tư thế...")

        ser.write(b's') # Gửi lệnh Start sang ESP32
        time.sleep(1)
        ser.reset_input_buffer()

        fieldnames = ["Timestamp", "AccX", "AccY", "AccZ", "Heart_IR", "Phase"]
        
        with open(filepath, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            global_start = time.time()
            data_row = {}

            for phase in phases:
                p_name, p_dur, p_val = phase["n"], phase["d"], phase["p"]
                p_start = time.time()
                
                print(f"\n\n--- CURRENT PHASE: {p_name} ({p_dur}s) ---")
                
                while (time.time() - p_start) < p_dur:
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8', errors='ignore').strip()
                        if line.startswith(">"):
                            parts = line[1:].split(":")
                            if len(parts) == 2: data_row[parts[0]] = parts[1]

                    # Triggered by AccZ (được gửi cuối cùng từ main.cpp)
                    if all(k in data_row for k in ["AccX", "AccY", "AccZ", "Heart_IR"]):
                        data_row["Timestamp"] = time.time() - global_start
                        data_row["Phase"] = p_val # Labeling chính xác theo phase
                        writer.writerow(data_row)
                        
                        # --- COUNTDOWN VÀ STATUS (Y HỆT BẢN GỐC CỦA CẬU) ---
                        rem = p_dur - (time.time() - p_start)
                        status = "OK" if int(data_row["Heart_IR"]) < 262143 else "⚠️ SAT!"
                        
                        if rem <= 3:
                            print(f"  [ NEXT PHASE IN ] {int(rem)+1}...  (IR: {data_row['Heart_IR']} {status})", end='\r')
                        else:
                            print(f"  Recording {p_name}: {int(rem)}s left (IR: {data_row['Heart_IR']} {status})", end='\r')
                        data_row = {}

        print(f"\n\n[SUCCESS] Session completed! Đã lưu tại: {filename}")
        ser.write(b'r') # Gửi lệnh Restart/Stop cho ESP32

    except KeyboardInterrupt:
        if 'ser' in locals(): ser.write(b'r')
        print(f"\n\n[STOPPED] Dừng khẩn cấp. Data đã lưu tại: {filepath}")
    except Exception as e:
        print(f"\n[ERROR] {e}")
    finally:
        if 'ser' in locals(): ser.close()

if __name__ == "__main__":
    collect()