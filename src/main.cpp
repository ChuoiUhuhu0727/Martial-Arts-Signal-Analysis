#include <Arduino.h>
#include <Wire.h>
#include "MAX30105.h"

MAX30105 particleSensor;
const int MPU_ADDR = 0x68; 

void setup() {
  Serial.begin(115200);
  delay(3000);
  Wire.begin(8, 9);
  
  // Khởi tạo IMU
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x1C); // Địa chỉ của ACCEL_CONFIG
  Wire.write(0x18); // Giá trị 0x18 tương ứng với +/- 16g 
  Wire.endTransmission(true);

  if (particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    particleSensor.setup(); 
    particleSensor.setPulseAmplitudeRed(0x0A);
    particleSensor.setPulseAmplitudeIR(0x1F); // Tăng độ sáng LED IR một chút để nhạy hơn
  }
}

void loop() {
  // Đọc IMU
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 14, true);
  
  int16_t ax = Wire.read()<<8 | Wire.read();
  int16_t ay = Wire.read()<<8 | Wire.read();
  int16_t az = Wire.read()<<8 | Wire.read();
  for(int i=0; i<8; i++) Wire.read(); 

  long irValue = particleSensor.getIR();

  // TRUYỀN DATA
  Serial.printf(">AccX:%d\n", ax);
  Serial.printf(">AccY:%d\n", ay);
  Serial.printf(">AccZ:%d\n", az);
  
  // Tăng ngưỡng lên 70,000 để lọc sạch nhiễu "không ấn gì"
  if (irValue > 70000) { 
    Serial.printf(">Heart_IR:%ld\n", irValue);
  } else {
    Serial.printf(">Heart_IR:0\n"); // Trả về 0 khi không có tay
  }

  delay(20); 
}