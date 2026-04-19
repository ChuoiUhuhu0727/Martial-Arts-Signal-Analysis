/*
 * Project: Aikido Punch Tracker (Member 2 - Giang)
 * Location: /firmware/main.cpp
 * Description: Data collection for MPU6050 & MAX30102 on ESP32 S3
 */
#include <Arduino.h>
#include <Wire.h>
#include "MAX30105.h"

// --- SYSTEM CONFIGURATION ---
const int MPU_ADDR = 0x68;
MAX30105 ppgSensor;

unsigned long lastSampleTime = 0;
const int sampleInterval = 10; // 100Hz (1 sample every 10ms) [cite: 73]
bool isCollecting = false;     // Waiting for 's' command from Python

void setup() {
  Serial.begin(115200);
  
  // Wait for Serial connection (Important for S3 chips)
  while (!Serial) {
    delay(10);
  }

  // Initialize I2C (SDA=8, SCL=9 for Lolin S3 Mini)
  Wire.begin(8, 9); 

  // 1. MPU6050 INITIALIZATION
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B); // Power Management register
  Wire.write(0);    // Wake up sensor
  Wire.endTransmission(true);

  // SET RANGE TO +/- 16G (PREVENT CLIPPING) [cite: 74]
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x1C); // ACCEL_CONFIG register
  Wire.write(0x18); // Write 0x18 for +/- 16g full scale
  Wire.endTransmission(true);
  
  // 2. MAX30102 INITIALIZATION
  if (!ppgSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println(">Status:MAX30102_NOT_FOUND");
    while (1); 
  }

  // PPG SETUP (PREVENT SATURATION 262,143) 
  byte ledBrightness = 30;  // Adjust to 15 if values still exceed 200,000 
  byte sampleAverage = 4;   
  byte ledMode = 2;         // 2 = Red + IR
  int sampleRate = 100;     
  int pulseWidth = 411;     
  int adcRange = 4096;      

  ppgSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);

  // 3. SYSTEM STATUS MESSAGE
  delay(500);
  Serial.println("\n==================================");
  Serial.println(">Status:SYSTEM_READY");
  Serial.println(">Instruction: Send 's' to START, 'r' to RESTART");
  Serial.println("==================================");
}

void loop() {
  // Check for commands from Serial Monitor or Python script
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 's') {
      isCollecting = true;
      Serial.println(">Status:STREAMING_STARTED");
    } else if (cmd == 'r') {
      isCollecting = false;
      Serial.println(">Status:STREAMING_STOPPED");
      ESP.restart(); 
    }
  }

  // Only send data if 's' command has been received
  if (isCollecting) {
    unsigned long currentTime = millis();
    if (currentTime - lastSampleTime >= sampleInterval) {
      lastSampleTime = currentTime;

      // READ IMU DATA (6 bytes)
      Wire.beginTransmission(MPU_ADDR);
      Wire.write(0x3B);
      Wire.endTransmission(false);
      Wire.requestFrom((uint8_t)MPU_ADDR, (uint8_t)6);

      if (Wire.available() >= 6) {
        int16_t ax = (int16_t)((Wire.read() << 8) | Wire.read());
        int16_t ay = (int16_t)((Wire.read() << 8) | Wire.read());
        int16_t az = (int16_t)((Wire.read() << 8) | Wire.read()); // PUNCH DIRECTION (Z-axis)

        // READ PPG DATA (IR)
        long irValue = ppgSensor.getIR();

        // SEND DATA TO PYTHON (Format: >Key:Value) 
        // Note: AccZ is sent LAST to act as the row-trigger in Python
        Serial.print(">Heart_IR:"); Serial.println(irValue);
        Serial.print(">AccX:");     Serial.println(ax);
        Serial.print(">AccY:");     Serial.println(ay);
        Serial.print(">AccZ:");     Serial.println(az);
      }
    }
  }
}