# Hướng dẫn đọc phần code kèm báo cáo — Subsystem A (Activity Classifier)

Tài liệu này dành cho người đọc báo cáo muốn kiểm chứng các con số trong đó.
Mỗi con số được nêu trong báo cáo đều sinh ra từ một file cụ thể dưới đây, chạy
được bằng một lệnh, không cần thao tác thủ công.

**Nguyên tắc của toàn bộ pipeline:** dữ liệu thô không bao giờ được sửa bằng tay,
và file dữ liệu đã xử lý cũng không bao giờ được sửa bằng tay. Muốn đổi cách xử
lý thì sửa script rồi chạy lại. Nhờ vậy toàn bộ kết quả tái tạo được từ đúng bản
ghi gốc của thiết bị.

---

## 1. Nộp những file nào

### Nhóm A — Bắt buộc (bằng chứng trực tiếp cho từng con số trong báo cáo)

| File | Chứng minh cho | Mục nào của báo cáo |
| :--- | :--- | :--- |
| **`train_activity_classifier.html`** | **Bắt đầu đọc từ file này.** Bản xuất đầy đủ của notebook: code, kết quả, 6 biểu đồ. Mở bằng trình duyệt bất kỳ, không cần cài gì | Toàn bộ |
| `train_activity_classifier.ipynb` | Notebook gốc sinh ra file HTML trên — dành cho người muốn chạy lại từng bước | Section 1, 3 |
| `train_activity_classifier.py` | Bản script rút gọn — chạy một lệnh ra toàn bộ con số | Section 1, 3 |
| `check_accel_variance_by_activity.py` | std_mag tĩnh 23.3 vs động 365.0 (chênh 15.7×) | Section 2 |
| `check_majority_baseline.py` | Baseline 0.201 / 0.599 và biên vượt baseline +0.347 / +0.254 | Section 4 |
| `build_processed_dataset.py` | Cách dựng tập dữ liệu từ bản ghi gốc — nguồn gốc dữ liệu | Toàn bộ |
| `data/processed/master_dataset.csv` | Chính tập dữ liệu được dùng (20.258 dòng, 18 participant) | Toàn bộ |

### Nhóm B — Nên nộp kèm (chứng minh dữ liệu là thật và đo ở đâu ra)

| File | Vai trò |
| :--- | :--- |
| `firmware_ble/main.cpp` (dòng 738–750) | Nơi 4 đặc trưng được tính **trên thiết bị**, theo cửa sổ trượt 2.4s — chứng minh con số trong báo cáo là đo thật, không phải tính lại trên máy tính |
| `experiments/wrist/participant_log.csv` | Danh sách 18 participant và file phiên tương ứng |
| `experiments/wrist/session_manifest.csv` | Trạng thái từng phiên thu, gồm cả các phiên bị loại và lý do |
| `log_serial.py` | Công cụ lấy dữ liệu từ bộ nhớ flash của thiết bị về máy tính |

### Nhóm C — Không cần nộp

Các file sau thuộc phần khác của đồ án, không liên quan đến báo cáo này, nộp vào
chỉ làm loãng: `lms_denoise_mvp.py`, `log_ble.py`, `realtime_*.py`,
`visualize_*.py`, `capture_waveform.py`, `jetson_server/`, `dashboard/`.

`logo_cv_activity_features.py` là phiên bản thử nghiệm trước của
`train_activity_classifier.py` — chỉ nộp nếu muốn cho thấy quá trình làm, còn về
kết quả thì nó đã bị thay thế.

---

### Notebook chứa 7 bước, mỗi bước một câu hỏi

`train_activity_classifier.html` được viết để đọc tuần tự, không cần biết code:

| Bước | Câu hỏi | Biểu đồ |
| :--- | :--- | :--- |
| 1 | Dữ liệu từ đâu ra? | — |
| 2 | 4 đặc trưng đo được gì, không đo được gì? | Phân bố `std_mag` của 5 hoạt động + phóng to riêng 3 tư thế tĩnh |
| 3 | Model đạt bao nhiêu trên 5 lớp? | Ma trận nhầm lẫn |
| 4 | Gộp 3 tư thế tĩnh lại thì sao? | Ma trận trước/sau đặt cạnh nhau + accuracy từng người |
| 5 | 0.853 có thật sự tốt không? | Baseline vs phần model thực sự học được |
| 6 | Model học được quy tắc gì? | Vẽ cây quyết định |
| 7 | Xuất model nạp lên thiết bị | — |

Biểu đồ ở bước 2 là biểu đồ quan trọng nhất: nó cho thấy **trước khi chạy model** rằng
3 tư thế tĩnh không thể tách được, và phần còn lại của notebook chỉ xác nhận điều đó
bằng số.

---

## 2. Cách chạy lại toàn bộ kết quả

Yêu cầu: Python 3 với `pandas`, `numpy`, `scikit-learn`, `joblib`.
Chạy từ thư mục gốc của repo, theo đúng thứ tự sau.

**Bước 1 — Dựng lại tập dữ liệu từ bản ghi gốc** *(không bắt buộc; file kết quả
đã có sẵn trong `data/processed/`)*

```bash
python build_processed_dataset.py
```

**Bước 2 — Kết quả chính của báo cáo (Section 1 và 3)**

```bash
python train_activity_classifier.py
```

Cần thấy ở cuối output:

```
5-class mean accuracy: 0.548
3-class mean accuracy: 0.853
```

**Bước 3 — Bằng chứng nguyên nhân gốc (Section 2)**

```bash
python check_accel_variance_by_activity.py
```

Cần thấy: `ratio dynamic/static: 15.66x`

**Bước 4 — So sánh với baseline (Section 4)**

```bash
python check_majority_baseline.py
```

Cần thấy biên vượt baseline: `+0.3474` (5 lớp) và `+0.2535` (3 lớp).

Cả bốn script đều dùng `random_state=0` nên kết quả giống hệt nhau qua mọi lần
chạy — không có yếu tố ngẫu nhiên.

---

## 3. Bản đồ: con số trong báo cáo ↔ nơi sinh ra nó

| Con số trong báo cáo | Sinh ra từ |
| :--- | :--- |
| 0.548 — accuracy 5 lớp | `train_activity_classifier.py`, dòng "5-class mean accuracy" |
| 0.853 — accuracy 3 lớp | cùng file, dòng "3-class mean accuracy" |
| Recall từng lớp (lying 0.284 … running 0.782) | cùng file, khối "per-class recall" |
| Ma trận nhầm lẫn | cùng file, khối "pooled confusion matrix" |
| std_mag 23.3 / 365.0 / 15.7× | `check_accel_variance_by_activity.py` |
| Bảng std_mag từng hoạt động | cùng file, bảng "std_mag by activity" |
| Baseline 0.201 / 0.599 | `check_majority_baseline.py` |
| Biên vượt baseline +0.347 / +0.254 | cùng file, dòng "margin over baseline" |
| Cửa sổ 2.4s, 60 mẫu @ 25Hz, stride 0.4s | `firmware_ble/main.cpp:738-750` |
| 18 participant, 16.880 dòng sạch | mọi script đều in ở dòng đầu tiên |
| 68.2% / 46.8% (thử nghiệm per-axis) | `CHANGELOG.md`, các mục 2026-07-22 → 2026-07-28 |

---

## 3b. Subsystem B — khử nhiễu PPG cổ tay

Báo cáo: `5_Bao_cao_SubsystemB.docx`. Các script phải chạy **theo đúng thứ tự** này, vì
mỗi bước lật lại kết luận của bước trước.

| Bước | Lệnh | Trả lời câu hỏi gì |
| :--- | :--- | :--- |
| 1 | `python lms_denoise_mvp.py` | So sánh ban đầu — ra 26.95 / 26.96 / 29.83 / 29.96 bpm |
| 2 | `python check_ground_truth_sanity.py` | Thước đo tham chiếu có đúng không? (**không** — trượt ở 3/5 người) |
| 3 | `python hr_estimator_v2.py` | Thước đã sửa có qua được kiểm tra sinh lý không? (4/5, so với 2/5) |
| 4 | `python lms_denoise_v2.py` | Đo lại bằng thước mới — ra tỉ lệ đọc được 35.0% vs 9.6% |
| 5 | `python plot_filter_results_v2.py` | Sinh 2 biểu đồ tỉ lệ đọc được |

Cần thêm `scipy` và `matplotlib` ngoài các thư viện ở mục 2.

**Con số nên trích từ Subsystem B là *tỉ lệ đọc được nhịp tim*, không phải bảng MAE.**
Chỉ có 19–38 cửa sổ mà cả hai kênh cùng đọc được — quá ít để xếp hạng bốn bộ lọc.

| Con số trong báo cáo B | Sinh ra từ |
| :--- | :--- |
| 26.95 / 26.96 / 29.83 / 29.96 bpm | `lms_denoise_mvp.py` (kết quả cũ, đã bị bác bỏ) |
| Bảng nhịp tim theo hoạt động, 5 người | `check_ground_truth_sanity.py` |
| P17: đếm tay 155.6 vs thuật toán 77.0 | cùng file, phần chẩn đoán dạng sóng |
| Tỉ lệ khoảng lẻ/chẵn 1.03, biên độ 2.22 | cùng file, hàm `beat_diagnostics()` |
| v2: P17 = 156.9, P16 = 118.9 | `hr_estimator_v2.py` |
| 35.0% vs 9.6% và bảng quét ngưỡng | `lms_denoise_v2.py`, `plot_filter_results_v2.py` |

---

## 4. Vài lựa chọn về phương pháp, nói rõ để khỏi bị hiểu nhầm

**Loại bỏ dòng chuyển tiếp.** Mọi script phân tích đều bỏ các dòng có
`is_transition == 1` — đó là khoảng ~15 giây participant đang đổi tư thế, lúc
này nhãn ghi trong file chưa mô tả đúng việc cơ thể đang làm. Giữ lại sẽ đưa dữ
liệu sai nhãn vào cả tập train lẫn tập test. Sau khi lọc còn 16.880 dòng trên
tổng 20.258.

**Baseline được tính trên đúng tập dòng đó.** `check_majority_baseline.py` áp
dụng cùng bộ lọc, vì một baseline tính trên tập dòng khác với tập dùng để đo
accuracy thì hai con số không so được với nhau.

**Giữ lại các dòng gia tốc bất thường.** `build_processed_dataset.py` có đánh dấu
`is_outlier_spike` nhưng **không xoá** dòng nào. Mục tiêu là hoạt động được với
chuyển động thật ngoài đời, không phải với dữ liệu sạch kiểu phòng lab.

**Loại phiên thu không hợp lệ ngay từ cấu trúc thư mục.** Các phiên chạy thử
(thiết bị đặt trên bàn, không có người đeo) nằm ở thư mục riêng
`firmware_test_fixtures/` và script dựng dữ liệu không bao giờ đọc tới đó — xem
`session_manifest.csv` để biết trạng thái từng phiên và lý do loại.

---

## 5. Những gì báo cáo này **không** chứng minh

Nêu ra để tránh bị hiểu quá phạm vi:

- **Không** chứng minh model phân biệt được lying / sitting / standing. Ngược
  lại: báo cáo chứng minh bộ đặc trưng hiện tại **không thể** làm điều đó, và
  giải thích nguyên nhân toán học.
- **Không** đo độ chính xác nhịp tim (PPG) — đó là subsystem khác.
- **Không** đo độ trễ hay mức tiêu thụ điện khi chạy trên thiết bị.
- Con số 0.853 là ước lượng theo LOGO-CV trên 18 người, **không phải** kết quả
  thử nghiệm triển khai thực tế trên người dùng mới ngoài đời.

---

## 6. Ghi chú về ngôn ngữ

Chú thích trong code viết bằng tiếng Anh (thống nhất với toàn bộ repo và với
thông lệ chung của mã nguồn), còn báo cáo và tài liệu hướng dẫn này viết bằng
tiếng Việt.
