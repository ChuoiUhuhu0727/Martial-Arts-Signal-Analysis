# 🥋 Punch Intensity Tracker

Dự án thu thập và xử lý dữ liệu đa cảm biến (IMU + PPG) phục vụ nhận diện cường độ đòn đánh Aikido. Hệ thống chạy trên ESP32 S3 với tần số 100Hz.

## 🛠 Hardware Configuration
- **MCU:** ESP32 S3 (Lolin S3 Mini).
- **IMU:** MPU6050 - Cấu hình dải đo **±16g**.
- **PPG:** MAX30102 - IR ổn định ở mức **100k - 200k**.

## 📂 Project Structure
Dự án được tổ chức như sau để dễ dàng bàn giao:

- `data/`: Chứa dữ liệu Raw và Processed (Kèm Data Dictionary riêng).
- `firmware/`: Code C++ cho ESP32.
- `scripts/`: Script thu thập dữ liệu qua Serial.
- `notebooks/`: Các Notebook phân tích QC và xử lý Master Dataset.
- `docs/visual_qc/`: Ảnh đồ thị kiểm định chất lượng hiệp thu.
