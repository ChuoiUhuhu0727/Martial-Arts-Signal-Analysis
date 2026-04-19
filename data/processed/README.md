# 📖 Master Dataset Documentation

File `master_dataset_aikido.csv` là kết quả của việc hợp nhất 17+ hiệp thu chuẩn (CLEAN), đã qua tiền xử lý và dán nhãn cường độ.

## 📊 Data Dictionary
| Column | Unit | Description |
| :--- | :--- | :--- |
| **Timestamp** | Seconds | Thời gian tương đối (100Hz). |
| **AccX, Y, Z** | Raw LSB | Gia tốc thô (Z là trục đấm chính). |
| **Acc_Mag** | Raw LSB | Độ lớn tổng hợp $\sqrt{AccX^2 + AccY^2 + AccZ^2}$. |
| **Heart_IR** | Raw Value | Tín hiệu hồng ngoại thô (PPG). |
| **Phase** | Label | 0: Rest, 1: Punch, 2: Recovery. |
| **Intensity_Label** | Label | 1: Light, 2: Medium, 3: Intense/Fatigue. |

## 🧪 Collection Protocol & Quality Control
- **Protocols:** Các hiệp thu được thực hiện theo kịch bản thời gian nghiêm ngặt (Light/Medium/Intense).
- **QC Criteria:** Chỉ các hiệp không bị Clipping gia tốc và có tín hiệu tim ổn định (Heart_IR > 0) mới được đưa vào Master Dataset.
