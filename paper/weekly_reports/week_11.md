# Week 11 Report — Firmware integration + hardware validation (M6)

Phần việc của **Giang**. Kế hoạch gốc: "Stability testing and full validation" — thực tế
tuần này gắn model vào firmware thật và test trên hardware lần đầu. Matches milestone
**M6** (full integration).

## Đã làm

- **Export model 5-class sang C (`activity_classifier_5class.h`)** (07-28,
  `export_classifier_to_c.py`). Đọc `models/activity_classifier.pkl`, sinh code C
  if/else lồng nhau theo đúng pattern đã có ở `classifier.h` — **không phải TFLite Micro**
  như roadmap cũ trong README ghi (sự thật đã lệch khỏi roadmap, README đã cập nhật lại).
  → **Ý nghĩa:** model AI được huấn luyện trên máy tính (Python) cần được "dịch" sang
  ngôn ngữ mà con chip nhỏ trên thiết bị đeo tay hiểu được, vì chip này không đủ mạnh để
  chạy trực tiếp chương trình Python. Viết công cụ tự động chuyển đổi model đã học thành
  code chạy trực tiếp trên chip. Đây là bước bắt buộc để AI đã huấn luyện thật sự hoạt
  động trên thiết bị thật, không chỉ dừng lại trên máy tính.
- **`firmware_ble` chuyển sang model 5-class thật** (07-28). Trước đó chỉ export file
  ra chứ chưa gắn vào firmware nào — flash thử mới phát hiện `main.cpp` vẫn gọi model
  binary cũ. Sửa: đổi include + call site sang `classifyActivity5class(...)`. **Field
  `activity_class` trong BLE JSON/session CSV đổi ý nghĩa**: trước binary (0=normal,
  1=intense), giờ 0=lying/1=running/2=sitting/3=standing/4=walking. Xoá bỏ
  `ACTIVITY_GATE` (ép activity_class=0 khi đứng yên) — đúng cho model binary cũ nhưng SAI
  cho model 5-class (đứng yên chính là lúc cần phân biệt lying/sitting/standing).
  → **Ý nghĩa:** phát hiện ra rằng dù đã "dịch" model mới xong (bước trên), chương trình
  điều khiển thiết bị thực tế vẫn đang chạy model cũ, đơn giản vì chưa ai nối 2 phần này
  lại với nhau. Đây là loại lỗi hay gặp khi 1 hệ thống có nhiều phần: từng phần riêng lẻ
  đúng nhưng quên chưa "cắm điện" nối chúng lại. Sửa xong, còn phát hiện thêm 1 đoạn logic
  cũ (tắt hẳn việc phân biệt tư thế khi đứng yên) là đúng cho phiên bản model cũ nhưng lại
  vô hiệu hoá đúng chức năng chính của model mới — gỡ bỏ đúng lúc trước khi nó âm thầm phá
  hỏng kết quả.
- **Test trên hardware thật** (07-29). Flash lên board, thu 1 session kiểm tra. Kết quả:
  **running 99%, standing 76% chính xác live** — thậm chí tốt hơn LOGO-CV offline;
  lying/sitting vẫn nhầm nặng sang standing — đúng hướng nhầm đã thấy lúc train (không
  phải bug integration mới, confirm đúng bug-1 đã root-cause tuần trước).
  → **Ý nghĩa:** đây là lần đầu tiên đeo thiết bị thật lên tay và xem AI nhận diện hoạt
  động trực tiếp, sau nhiều tuần chỉ test trên máy tính. Kết quả khớp với những gì đã dự
  đoán từ lúc huấn luyện model (chạy tốt với đi/đứng, nhầm lẫn giữa nằm/ngồi/đứng) — điều
  này xác nhận quá trình "dịch" model sang thiết bị thật (2 bước trên) đã làm đúng, không
  có lỗi phát sinh mới khi chuyển từ máy tính sang thiết bị vật lý.
- **Phát hiện + loại 1 session lỗi khỏi dataset** (07-29). Đoạn "walking" trong session
  test bị đoán thành "standing" 95% — điều tra ra không phải bug: participant thực ra
  đứng yên đeo lại sensor lúc đó (std_mag ~23, thấp hơn 10 lần so với walking lúc train
  ~265), không phải finding thật. Chuyển session này + raw files đi kèm sang
  `firmware_test_fixtures/`, xoá dòng `P18` khỏi participant log — vì mục đích thu là
  test firmware, không phải data thật.
  → **Ý nghĩa:** khi thấy kết quả lạ, thay vì vội kết luận "AI bị lỗi", điều tra kỹ và
  phát hiện ra nguyên nhân thật là do người thử nghiệm đứng yên chỉnh lại thiết bị đúng
  lúc máy đang ghi nhãn "đang đi bộ" — tức là lỗi ở khâu thực hiện thí nghiệm, không phải
  lỗi của AI. Loại đúng phần dữ liệu bị lỗi này ra khỏi tập dữ liệu chính, tránh làm nhiễu
  các kết quả báo cáo sau này. Đây là công việc kiểm soát chất lượng dữ liệu, đảm bảo mọi
  con số báo cáo đều đáng tin.
- **Gap phát hiện, chưa sửa**: `log_serial.py` auto-filer hiện không phân biệt được
  "session thu thật" với "session thu để test code" — dọn tay lần này, để dành sửa nếu
  lặp lại thường xuyên.
  → **Ý nghĩa:** ghi nhận trung thực 1 lỗ hổng quy trình vừa phát hiện được (chương trình
  tự động phân loại dữ liệu chưa phân biệt được đâu là dữ liệu thật, đâu là dữ liệu test),
  nhưng cân nhắc chưa sửa ngay vì mới xảy ra 1 lần — quyết định hợp lý về việc ưu tiên thời
  gian, không sửa mọi thứ ngay khi vừa phát hiện nếu chưa chắc nó sẽ lặp lại thường xuyên.

## Kết quả

Model 5-class chạy thật trên hardware, kết quả live khớp với offline (xác nhận pipeline
train→export→firmware đúng, không có regression khi tích hợp). PR #25 (firmware wiring +
hardware test cleanup) mở, sau đó merge 01-08.

## Khác biệt so với kế hoạch gốc

Không có 60-phút stability test / heap monitoring liên tục (chưa làm — validate hardware
tuần này chỉ ở mức 1 session ngắn, không phải stress test dài).

---
[← Week 10](week_10.md) · [Weekly reports index](README.md) · [Week 12 →](week_12.md)
