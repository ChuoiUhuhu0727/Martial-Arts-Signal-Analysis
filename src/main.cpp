#include <Arduino.h>
#include <Wire.h>
#include "MAX30105.h"

// Địa chỉ và Đối tượng
const int MPU_ADDR = 0x68;
MAX30105 ppgSensor;

// Quản lý thời gian (Sampling Rate)
unsigned long lastSampleTime = 0;
const int sampleInterval = 10; // 100Hz cho IMU

void setup() {
  Serial.begin(115200);
  Wire.begin(8, 9); 

  // 1. Khởi tạo MPU6050 (Dựa trên code hiện tại của cậu)
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B); Wire.write(0); Wire.endTransmission(true);
  
  // 2. Khởi tạo & Cấu hình MAX30102
  if (!ppgSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println(">Status:MAX30102_NotFound");
    while (1);
  }

  // Cấu hình LED cho MAX30102 (Quan trọng để có data IR)
  byte ledBrightness = 60; // 0=Off to 255=50mA
  byte sampleAverage = 4;  // 1, 2, 4, 8, 16, 32
  byte ledMode = 2;        // 1 = Red only, 2 = Red + IR
  int sampleRate = 100;    // 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411;    // 69, 118, 215, 411
  int adcRange = 4096;     // 2048, 4096, 8192, 16384

  ppgSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);
}

void loop() {
  // Thực hiện đọc dữ liệu theo chu kỳ cố định
  if (millis() - lastSampleTime >= sampleInterval) {
    lastSampleTime = millis();

    // --- KHỐI ĐỌC MPU6050 ---
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B);
    Wire.endTransmission(false);
    Wire.requestFrom((uint8_t)MPU_ADDR, (uint8_t)6);

    if (Wire.available() >= 6) {
      int16_t ax = (Wire.read() << 8) | Wire.read();
      int16_t ay = (Wire.read() << 8) | Wire.read();
      int16_t az = (Wire.read() << 8) | Wire.read();

      // --- KHỐI ĐỌC MAX30102 ---
      // Lấy giá trị hồng ngoại (IR)
      long irValue = ppgSensor.getIR();

      // --- KHỐI GỬI DỮ LIỆU (Theo định dạng script Python yêu cầu) ---
      // Lưu ý: Heart_IR nên gửi trước AccZ để Python bắt đủ bộ
      Serial.print(">Heart_IR:"); Serial.println(irValue);
      Serial.print(">AccX:");     Serial.println(ax);
      Serial.print(">AccY:");     Serial.println(ay);
      Serial.print(">AccZ:");     Serial.println(az);
    }
  }
}