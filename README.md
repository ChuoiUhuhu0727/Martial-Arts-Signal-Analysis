# Martial Arts Performance & Heart Rate Recovery Analysis

## 📌 Project Overview
This project is part of the **ENG209: Signals, Systems and Control** course at Fulbright University Vietnam. Our system analyzes martial arts punch intensity and evaluates fitness levels through heart rate recovery post-exercise.

### Key Features:
**Punch Force Estimation:** Capturing 3-axis acceleration using MPU6050.
**PPG Signal Analysis:** Monitoring heart rate and recovery speed with MAX30102.
**Real-time Visualization:** Waveform display of strike impact and heart rate.
**Fitness Classification:** Using ML to categorize fitness as Excellent, Average, or Poor.

---

## 👥 The Team (Team 209-Spring 2026)
| Name | Major | [cite_start]Primary Responsibilities|
| :--- | :--- | :--- |
| **Tran Thanh Tung** | Engineering | Hardware & DSP (Sensor integration, Filter design) |
| **Hoang Nguyen Ngoc Giang** | Computer Science | Software & Integration (Firmware, FFT, Python GUI) |
| **Phan Ngoc Quoc Duy** | Engineering | AI & Documentation (Feature extraction, ML Model) |

---

## 🛠 Hardware Architecture
**Microcontroller:** Xiao ESP32-S3
**Sensors:** 
* MAX30102 (Pulse Oximeter & Heart-Rate Sensor)
* MPU6050 (6-axis IMU)

---

## 📈 Roadmap & Progress Checkpoints
- [ ] **Week 12: Progress Check 1** - Sensor acquisition verified, raw signal plots, and initial FFT.
- [ ] **Week 14: Progress Check 2** - End-to-end pipeline integration, filter implementation, and ML model training.
- [ ] **Week 16: Final Presentation** - Live demo and final report submission.

---

## 📂 Project Structure
* `/src`: ESP32 firmware and main logic.
* `/notebooks`: Python notebooks for PPG/IMU signal analysis and ML training.
* `/data`: Raw datasets for heart rate and punch intensity.
* `/docs`: Project registration form and progress reports.
