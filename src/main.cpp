#include <Arduino.h>
#include <Wire.h>
#include "MAX30105.h"

// Địa chỉ và Đối tượng
const int MPU_ADDR = 0x68;
MAX30105 ppgSensor;

// Quản lý thời gian (Sampling Rate)
unsigned long lastSampleTime = 0;
const int sampleInterval = 10; // 100Hz (Cực kỳ quan trọng để bắt cú đấm Aikido)

void setup() {
  Serial.begin(115200);
  Wire.begin(8, 9); // SDA=8, SCL=9 cho Lolin S3 Mini

  // 1. KHỞI TẠO MPU6050
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B); // Thanh ghi PWR_MGMT_1
  Wire.write(0);    // Đánh thức cảm biến
  Wire.endTransmission(true);

  // --- SỬA LỖI CLIPPING TẠI ĐÂY ---
  // Cấu hình +/- 16g (Thanh ghi 0x1C, ghi giá trị 0x18)
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x1C); 
  Wire.write(0x18); 
  Wire.endTransmission(true);
  
  // 2. KHỞI TẠO MAX30102
  if (!ppgSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println(">Status:MAX30102_NotFound");
    while (1);
  }

  // --- SỬA LỖI SATURATION 262143 TẠI ĐÂY ---
  // Hạ ledBrightness xuống để tránh bão hòa (Saturation)
  byte ledBrightness = 30;  // Giảm từ 60 xuống 30 (khoảng 6.4mA) để tránh "lóa"
  byte sampleAverage = 4;   // Lấy mẫu trung bình 4 lần để làm mượt raw data
  byte ledMode = 2;         // 2 = Red + IR
  int sampleRate = 100;     // 100 samples per second
  int pulseWidth = 411;     // Độ rộng xung (ảnh hưởng đến độ phân giải ADC)
  int adcRange = 4096;      // ADC range 18-bit

  ppgSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);
}

void loop() {
  // Thực hiện đọc dữ liệu theo chu kỳ cố định (Non-blocking)
  if (millis() - lastSampleTime >= sampleInterval) {
    lastSampleTime = millis();

    // --- KHỐI ĐỌC MPU6050 ---
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B);
    Wire.endTransmission(false);
    Wire.requestFrom((uint8_t)MPU_ADDR, (uint8_t)6);

    if (Wire.available() >= 6) {
      // Đọc và ép kiểu về int16_t để Python nhận đúng số âm/dương
      int16_t ax = (int16_t)((Wire.read() << 8) | Wire.read());
      int16_t ay = (int16_t)((Wire.read() << 8) | Wire.read());
      int16_t az = (int16_t)((Wire.read() << 8) | Wire.read());

      // --- KHỐI ĐỌC MAX30102 ---
      long irValue = ppgSensor.getIR();

      // --- KHỐI GỬI DỮ LIỆU ---
      // Gửi Heart_IR trước, AccZ cuối cùng để Trigger ghi dòng trong Python
      Serial.print(">Heart_IR:"); Serial.println(irValue);
      Serial.print(">AccX:");     Serial.println(ax);
      Serial.print(">AccY:");     Serial.println(ay);
      Serial.print(">AccZ:");     Serial.println(az);
    }
  }
}