# Martial Arts Performance & Heart Rate Recovery Analysis

## 📌 Project Overview
[cite_start]This project is part of the **ENG209: Signals, Systems and Control** course at Fulbright University Vietnam[cite: 1, 2]. [cite_start]Our system analyzes martial arts punch intensity and evaluates fitness levels through heart rate recovery post-exercise[cite: 8].

### Key Features:
* [cite_start]**Punch Force Estimation:** Capturing 3-axis acceleration using MPU6050[cite: 8].
* [cite_start]**PPG Signal Analysis:** Monitoring heart rate and recovery speed with MAX30102[cite: 8].
* [cite_start]**Real-time Visualization:** Waveform display of strike impact and heart rate[cite: 8].
* [cite_start]**Fitness Classification:** Using ML to categorize fitness as Excellent, Average, or Poor[cite: 8].

---

## 👥 The Team (Team 209-Spring 2026)
| Name | Major | [cite_start]Primary Responsibilities [cite: 4, 34] |
| :--- | :--- | :--- |
| **Tran Thanh Tung** | Engineering | Hardware & DSP (Sensor integration, Filter design) |
| **Hoang Nguyen Ngoc Giang** | Computer Science | Software & Integration (Firmware, FFT, Python GUI) |
| **Phan Ngoc Quoc Duy** | Engineering | AI & Documentation (Feature extraction, ML Model) |

---

## 🛠 Hardware Architecture
* [cite_start]**Microcontroller:** Xiao ESP32-S3 [cite: 12]
* [cite_start]**Sensors:** * MAX30102 (Pulse Oximeter & Heart-Rate Sensor) [cite: 12]
  * [cite_start]MPU6050 (6-axis IMU) [cite: 12]

---

## 📈 Roadmap & Progress Checkpoints
- [ ] [cite_start]**Week 12: Progress Check 1** - Sensor acquisition verified, raw signal plots, and initial FFT[cite: 17].
- [ ] [cite_start]**Week 14: Progress Check 2** - End-to-end pipeline integration, filter implementation, and ML model training[cite: 17].
- [ ] [cite_start]**Week 16: Final Presentation** - Live demo and final report submission[cite: 39].

---

## 📂 Project Structure
* `/src`: ESP32 firmware and main logic.
* `/notebooks`: Python notebooks for PPG/IMU signal analysis and ML training.
* `/data`: Raw datasets for heart rate and punch intensity.
* `/docs`: Project registration form and progress reports.
