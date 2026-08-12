# Week 12 Report — Dataset finalized (N=18), secondary 3-class finding, report skeletons

Phần việc của **Giang**. Kế hoạch gốc: "External user testing and final iteration" —
thực tế tuần này là hoàn thiện dataset và tìm thêm 1 finding phụ, cộng chuẩn bị khung sườn
báo cáo cho 2 track.

## Đã làm

- **Thêm P18 (participant thật, khác với session test đã loại ở Week 11)** — dataset lên
  **N=18**.
- **Finding phụ: regroup 3-class (stationary/walking/running)** (~07-30). Cùng model
  (`DecisionTreeClassifier(max_depth=5, min_samples_leaf=5)`), cùng 4 feature, cùng
  dataset, cùng protocol LOGO-CV — chỉ đổi cột target (`label` → `activity_group`, gộp
  lying/sitting/standing thành `stationary`). **Kết quả: 0.853 accuracy** (per-class
  recall: stationary 0.951, walking 0.632, running 0.777) — so với 0.548 của 5-class.
- **Quyết định giữ 5-class làm số báo cáo chính**, không thay bằng 3-class — 3-class được
  báo cáo như 1 finding phụ đi kèm, không phải bản thay thế (vì 5-class giữ được thông
  tin lying/sitting/standing dù kém chính xác hơn, có giá trị thực tế hơn cho ứng dụng
  cuối).

### Technical story: gộp 3-class có phải cherry-picking không?

Input chỉ có 4 feature và 18 participant — tập dữ liệu khá nhỏ, dễ overfit nếu để
decision tree rẽ nhánh sâu; đó là lý do model vẫn giữ `max_depth=5, min_samples_leaf=5`
thay vì để cây tự do phát triển, kể cả sau khi đổi target.

Việc gộp lying/sitting/standing thành 1 lớp `stationary` **không phải chọn nhãn ngẫu
nhiên rồi tình cờ ra số đẹp hơn** — nó nối thẳng với cơ chế đã tìm ra ở tuần trước
(bug-1): cả 4 feature đều là hàm của magnitude, mà magnitude bất biến với rotation nên
không phân biệt được 3 tư thế chỉ khác nhau ở *orientation*. Đây là giới hạn *cấu trúc*
của chính bộ feature, không phải lỗi ngẫu nhiên có thể vá bằng cách đổi nhãn. Gộp 3 lớp
đó lại loại bỏ đúng phần mà bộ feature này *về nguyên lý không thể* phân biệt, trong khi
vẫn giữ nguyên phân biệt giữa 3 nhóm còn lại (stationary/walking/running) — nơi magnitude
*có* khác biệt rõ, vì đó là khác biệt ở cường độ chuyển động, đúng thứ magnitude đo được.
Vì vậy bước nhảy 0.548 → 0.853 phản ánh đúng việc loại bỏ 1 giới hạn đã root-cause được
từ tuần trước, không phải một phép thử ngẫu nhiên may mắn ra kết quả tốt.
- **Khung sườn báo cáo** — `paper/activity_classifier_report_OUTLINE.md` (skeleton, số đã
  verify sẵn để trích) và `paper/adaptive_filter_comparison_2026-07-28.md` (draft đầy đủ
  cho track LMS/RLS/Wiener) được tạo, làm nguyên liệu cho Week 13.
- **PR #26 merge** (01-08) — chốt lại tài liệu tiến độ 30-07 (N=18, classifier
  deployed+validated, report tooling).

## Kết quả

Dataset cuối cùng: **N=18 participant**. 2 con số chính thức để báo cáo: 5-class 0.548
(primary), 3-class 0.853 (secondary finding).

## Khác biệt so với kế hoạch gốc

Không có external user testing (3 người ngoài team) — dataset hiện tại đều là participant
nội bộ/quen biết, chưa test với người hoàn toàn ngoài dự án.

---
[← Week 11](week_11.md) · [Weekly reports index](README.md) · [Week 13 →](week_13.md)
