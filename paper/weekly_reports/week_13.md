# Week 13 Report — Report writing: activity classifier + adaptive filter comparison

Phần việc của **Giang**. Kế hoạch gốc: "Documentation and final demo" — tuần này đúng
đúng theo kế hoạch: viết report kỹ thuật, dù chưa phải bản final writeup 1000–1500 từ.

## Đã làm

- **Subsystem B (`paper/adaptive_filter_comparison_2026-07-28.md`) chuyển thành outline**
  (12-08). File đầy đủ trước đó do Claude viết hoàn toàn — vì đây cũng là báo cáo nộp chấm
  điểm (giống subsystem A), chuyển thành `adaptive_filter_comparison_OUTLINE.md` (số liệu
  giữ nguyên, phần phân tích để tự viết), giữ file gốc lại làm tài liệu tham chiếu, đánh
  dấu rõ "NOT FOR SUBMISSION".
- **Subsystem A (`paper/activity_classifier_report_OUTLINE.md`) hoàn thiện từng phần**:
  - Section 1 (LOGO-CV + per-class recall) — **Giang tự viết** qua Socratic Q&A, tự tính
    ra: lying (0.283) cao hơn đoán mò (0.20) nhưng thấp hơn hẳn average (0.548); chỉ lying
    thấp hẳn, sitting/standing vẫn ở mức tương đương average.
  - Section 2 (root cause 4 feature + 3 alternative per-axis) — Giang viết phần định
    nghĩa lại 4 feature và 3 hướng thử, Claude sửa scope error (window 2.4s không phải cả
    hiệp 90s) + bổ sung 2 đoạn còn thiếu (công thức bất biến rotation; đối chiếu evidence
    thật 68.2%/P03 46.8% cho hypothesis lật cổ tay — bị bác bỏ vì không giải thích được
    tại sao chỉ P03 fail).
  - Section 3–5 — **Claude viết** theo yêu cầu trực tiếp của Giang (không qua Socratic),
    dùng số liệu thật tính bằng script mới `check_majority_baseline.py` (majority-baseline
    5-class=0.201, 3-class=0.599 — cho thấy so sánh thẳng 0.548 vs 0.853 hơi đánh lừa).
- **Ý tưởng 2-layer model** (Giang tự đề xuất, section 5): tách model tĩnh (dùng gyro) và
  model động (giữ decision tree cũ) thay vì 1 model 5-class duy nhất — rẻ hơn phương án
  gyro+calibration ban đầu vì không cần protocol calibration riêng.

### Technical story: so sánh 0.548 vs 0.853 trực tiếp có công bằng không?

Viết `check_majority_baseline.py` để trả lời câu hỏi "cải thiện 0.548→0.853 có ý nghĩa
không" bằng số thật thay vì cảm tính. Kết quả: majority-class baseline của 5-class chỉ
0.201 (dataset gần cân bằng, gần bằng đoán mò 1/5=0.20), nhưng của 3-class lên tới 0.599
— vì lớp `stationary` gộp 3/5 lớp gốc nên chiếm đa số áp đảo, chỉ cần đoán "stationary"
cho mọi trường hợp đã đúng gần 60%. Điều này có nghĩa: **so sánh thẳng 0.548 vs 0.853
(+0.305) hơi đánh lừa** — một phần con số 0.853 cao là vì bài toán 3-class *dễ hơn do
cấu trúc* của chính nó, không hoàn toàn vì model học tốt hơn. Thước đo công bằng hơn là
margin trên baseline riêng của từng bài toán: 5-class hơn baseline của nó +0.347, 3-class
hơn baseline của nó +0.254 — 3-class vẫn thắng rõ (gấp ~1.4 lần baseline riêng), nhưng
biên độ cải thiện thực chất nhỏ hơn con số +0.305 thô cho thấy.

**Ý tưởng 2-layer model** ra đời khi cân nhắc lại đề xuất gyro+calibration (phương án
tốn nhất — đổi cả firmware, protocol, và không dùng lại được 18 participant hiện có vì
không ai có data gyro/calibration). Alternative rẻ hơn: tách model 5-class hiện tại
thành 2 lớp — lớp "động" (walking/running) giữ nguyên decision tree + 4 feature cũ (đã
hoạt động tốt, recall 0.639/0.771), lớp "tĩnh" (lying/sitting/standing) dùng trục gyro
(có sẵn trên MPU6050, chưa đọc) để bắt *chuyển động đổi tư thế* (VD: nằm→ngồi có 1 đoạn
xoay rõ trên gyro, dù magnitude accel gần như không đổi) thay vì dựa vào accel magnitude
tĩnh — không cần bước calibration riêng cho mỗi người, chỉ cần đọc thêm 1 cảm biến đã có
sẵn phần cứng.

## Kết quả

2 outline báo cáo (subsystem A, B) hoàn chỉnh nội dung, sẵn sàng review lại trước khi nộp.
1 script mới (`check_majority_baseline.py`) checked-in, re-runnable.

## Khác biệt so với kế hoạch gốc

Chưa có: technical writeup 1000–1500 từ hoàn chỉnh, GitHub README test bởi người ngoài,
demo video. Đây là bước report-writing giữa chừng, không phải final writeup.

---
[← Week 12](week_12.md) · [Weekly reports index](README.md)
