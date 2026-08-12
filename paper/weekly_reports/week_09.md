# Week 9 Report — Pipeline automation, bug-1 closed, classifier trained (M3)

Phần việc của **Giang**. Kế hoạch gốc: "Integration debugging and stress testing" —
thực tế tuần này là bước ngoặt: tự động hoá pipeline, đóng lại bug-1, và train ra
classifier đầu tiên. Matches milestone **M3** (model trained + exported).

## Đã làm

- **`log_serial.py` tự phân loại session + tự đề xuất participant_id** (07-28). Sau mỗi
  lần retrieve, tự áp rule dry-run + check độ đầy đủ, tự dời file (dry-run →
  `firmware_test_fixtures/`, hoàn chỉnh → `valid_sessions/` + tự thêm dòng vào
  `participant_log.csv`). `participant_id` tự đoán số P tiếp theo — đánh đổi tốc độ lấy
  rủi ro sai nhỏ (sửa sau dễ hơn dựng lại participant log từ đầu).
- **`build_processed_dataset.py`** (07-28) — script mới build `data/processed/master_dataset.csv`
  từ `valid_sessions/` + `participant_log.csv`, tự thêm cột `activity_group` (gộp
  lying/sitting/standing → `stationary`) để train được cả model 3-class lẫn 5-class không
  cần chạy lại script.
- **Thêm P16/P17 (2 participant mới, dual-PPG đầy đủ)** (07-28) — dataset lên **N=17**.
- **Bug-1 re-check tại N=6** (thêm P16/P17 vào pool raw-capture): kết quả **phức tạp hơn,
  không giải quyết được** — biến thể raw-enhanced làm P04 tệ đi (62.2%→35.0%), P16 là
  participant tệ nhất với biến thể relative-baseline (29.6%, tệ hơn cả baseline).
- **Quyết định đóng bug-1 rabbit hole** (07-28): sau 3 biến thể per-axis thử ở N=4→6
  không có biến thể nào generalize sạch, dừng thử thêm feature-engineering trên data đã
  có. **Giữ 5-class** (không gộp 3-class) — coi lying/sitting/standing confusion là finding
  đã root-cause (magnitude không mang thông tin hướng đeo), báo cáo trung thực thay vì vá
  tiếp. Hướng fix thật (calibration step + gyro) parked cho lần thu data tương lai.
- **Đánh giá đề xuất AI-model của advisor** (07-28): PPG+IMU→HR end-to-end được đánh giá
  là ý hay nhưng cần nhiều participant hơn project hiện có (literature ~15 participant,
  project có 5 dual-PPG) — giữ nguyên plan classical-filter, coi AI-model là hướng so sánh
  thêm sau, không thay thế.
- **Repo cleanup** (07-28) — dọn file/build artifact không dùng vào `archived/`.
- **`train_activity_classifier.py`** (07-28) — train 5-class DecisionTree (LOGO-CV,
  N=17). **Kết quả: mean accuracy 0.547**, lying/sitting/standing confuse nặng (lying
  recall 0.283 — đúng root cause bug-1), walking/running tách tốt (0.639/0.771).

### Technical story: đánh giá bằng LOGO-CV, và tại sao 1 con số accuracy không đủ

Đánh giá model bằng **LOGO-CV (leave-one-group-out)**: khác với chia train/test ngẫu
nhiên theo dòng, mỗi participant lần lượt bị cho ra rìa làm test set — để đo model có
học vẹt đặc điểm của từng người hay thật sự tổng quát hoá được sang người chưa từng
thấy. Lặp lại cho đến khi mọi participant đều 1 lần làm test set, rồi lấy trung bình.

Con số 0.547 trung bình dễ gây hiểu lầm là model "khá đều" trên cả 5 lớp. Nhìn per-class
recall thì không phải vậy: lying chỉ 0.283 — cao hơn đoán mò (1/5 = 0.20 cho bài toán
5-class cân bằng) nhưng chỉ nhỉnh hơn một chút, trong khi sitting (0.490) và standing
(0.548) không hề thấp — standing thậm chí bằng đúng average. Tức là model không tệ đều:
chỉ riêng lying gần như đoán mò, còn lại vẫn ở mức chấp nhận được. Nếu chỉ báo cáo
0.547 sẽ che mất chỗ yếu thật của model.

**Vì sao lying/sitting/standing (3 tư thế tĩnh) lại khó phân biệt trong khi walking/
running (2 hoạt động động) thì không** — cả 4 feature đưa vào model (`mean_mag`,
`std_mag`, `peak_max`, `peak_rel`) đều là hàm số của **magnitude** gia tốc, tức
`sqrt(ax² + ay² + az²)`. Đây chính là độ dài (norm) của vector gia tốc — khi thiết bị bị
xoay (đổi hướng đeo), phép xoay chỉ đổi *hướng* của vector, không đổi *độ dài* của nó.
Nên dù từng trục ax/ay/az đổi giá trị theo hướng xoay, magnitude vẫn giữ nguyên — tức là
4 feature này **không mang thông tin hướng đeo (orientation)**, chỉ phản ánh cường độ
chuyển động. Lying/sitting/standing khác nhau đúng ở orientation (nằm/ngồi/đứng là 3
hướng khác nhau của cùng 1 trạng thái gần như đứng yên), không khác ở cường độ chuyển
động — nên bộ feature hiện tại về nguyên lý không thể tách được 3 lớp này. Walking/
running thì khác nhau rõ ở *cường độ* (magnitude dao động mạnh khi chạy hơn khi đi) —
đúng thứ magnitude đo được, nên 2 lớp này tách tốt.

**3 hướng per-axis từng thử trước đó (23/7–28/7) không generalize được**, và tuần này
mới làm rõ được cơ chế thật: hypothesis ban đầu là raw device-frame nhạy với "lật cổ
tay trong lúc vận động" — nhưng đối chiếu số liệu thật thì không khớp: raw per-axis đạt
68.2% ở N=4, nhưng riêng P03 rớt còn 46.8% (ngang baseline), 3 người còn lại vẫn 68.2%.
Nếu cơ chế là lật-cổ-tay-trong-lúc-vận-động, nó phải ảnh hưởng **đều tất cả participant**
như nhau — không giải thích được vì sao chỉ P03 fail. Bác bỏ hypothesis đó; cơ chế đúng
hơn là mỗi người đeo thiết bị ở 1 góc *cố định* khác nhau — khác nhau *giữa người*, không
phải lật cổ tay trong lúc đo — đúng với "wearing-angle confound" mà bug-1 rabbit hole gặp
phải ở cả 3 biến thể per-axis đã thử.

## Kết quả

Pipeline thu→xử lý→train chạy được từ đầu đến cuối không cần sửa tay giữa các bước.
Bug-1 chính thức đóng lại như 1 finding đã giải thích được, không phải bug tồn đọng.
Model 5-class đầu tiên: **0.547 accuracy (LOGO-CV, N=17)**.

## Khác biệt so với kế hoạch gốc

Không có "3 full 30-minute sessions" stress test trên hardware tích hợp (chưa có
PCB/enclosure tích hợp — xem Week 11 cho phần validate trên hardware thật).

---
[← Week 8](week_08.md) · [Weekly reports index](README.md) · [Week 10 →](week_10.md)
