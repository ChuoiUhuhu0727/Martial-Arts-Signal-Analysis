# Week 6 Report — Data-collection pipeline hardening

Phần việc của **Giang**. Kế hoạch gốc: "Model training, quantization, and PCB order" —
thực tế chưa có đủ data để train, tuần này tiếp tục làm chắc pipeline thu thập trước.

## Đã làm

- **Fix: `ppgOK` là flag tĩnh (boot-time) → đổi thành `ppg_contact` sống theo từng dòng**
  (07-14). Field cũ chỉ set 1 lần lúc `setup()`, chưa từng bắt được mất-contact thật.
  Giờ tính lại mỗi window, ghi vào cả flash CSV lẫn BLE payload.
  → **Ý nghĩa:** cảm biến đo nhịp tim cần áp sát da mới đo đúng. Trước đó hệ thống chỉ
  kiểm tra "cảm biến có áp da không" đúng 1 lần lúc mới bật máy, rồi coi như đúng suốt cả
  buổi đo — dù người tham gia có thể làm lệch cảm biến giữa chừng mà hệ thống không hề
  biết. Sửa để kiểm tra liên tục theo thời gian thực, giúp phát hiện đúng lúc cảm biến bị
  lệch thay vì phát hiện sau khi dữ liệu đã hỏng.
- **Protocol: thêm 15s prep trước hoạt động 1; âm thanh báo hiệu chuyển sang phát từ
  laptop** (07-14). Trước đó recording bắt đầu ngay lúc boot, participant không kịp vào
  tư thế "lying" đầu tiên. Buzzer phần cứng bị bỏ (né bug im lặng khi chạy pin, chưa fix).
  → **Ý nghĩa:** trước đó máy bắt đầu ghi dữ liệu ngay khi vừa bật, người tham gia chưa
  kịp nằm xuống thì máy đã tính là "đang nằm" — gắn nhãn sai ngay từ giây đầu tiên. Thêm
  15 giây chuẩn bị trước khi bắt đầu tính, và chuyển âm thanh nhắc chuyển động tác sang
  phát từ máy tính (thay vì loa nhỏ gắn trên thiết bị đang gặp lỗi khi chạy pin) để người
  tham gia luôn biết rõ khi nào cần đổi tư thế. Trực tiếp cải thiện độ chính xác của nhãn
  dữ liệu — nền tảng để AI học đúng.
- **Dump không cần reset nữa: on-demand trigger qua Serial** (07-14). Board trong
  enclosure không bấm nút reset được; `task_classifier` giờ lắng nghe ký tự Serial mỗi
  vòng lặp, trigger dump ngay sau khi 5 hoạt động xong (`protocolFinished`).
  → **Ý nghĩa:** trước đó phải bấm 1 nút vật lý trên thiết bị để lấy dữ liệu ra sau mỗi
  buổi đo — nhưng khi thiết bị được lắp vào vỏ hộp (enclosure) thì nút đó bị che mất, không
  bấm được nữa. Sửa để có thể ra lệnh lấy dữ liệu từ máy tính, không cần chạm vào thiết
  bị. Giúp quy trình lấy dữ liệu sau mỗi buổi đo nhanh và ít rủi ro hỏng hóc hơn.
- **Ngưỡng detect nhịp thích nghi + cột `bpm_fresh`** (07-15). BPM bị đứng yên hàng chục
  giây ở nhiều file do ngưỡng AC cố định — sửa thành ngưỡng co giãn theo biên độ sóng gần
  nhất. Thêm cột `bpm_fresh` đánh dấu khi nào 1 nhịp thật sự vừa được detect.
  → **Ý nghĩa:** hệ thống đo nhịp tim bằng cách nhận diện từng nhịp đập qua tín hiệu ánh
  sáng phản xạ trên da. Ngưỡng nhận diện cũ là 1 con số cố định, không phù hợp với biên độ
  tín hiệu khác nhau ở từng người/từng lúc — dẫn đến có lúc máy "không thấy nhịp nào" cả
  chục giây dù tim vẫn đập bình thường. Sửa để ngưỡng tự điều chỉnh theo tín hiệu thực tế
  của từng người, đo nhịp tim chính xác và liên tục hơn — 1 trong 2 kết quả đầu ra chính
  của cả sản phẩm (cùng với nhận diện hoạt động).
- **Thêm raw waveform capture (task + queue riêng) cho hướng nghiên cứu LMS** (07-15).
  BPM đã tính sẵn không đủ để so sánh LMS/RLS/Wiener — cần chạy thuật toán trên raw
  signal. Thêm `task_raw_writer`, ghi `/raw_ppg_N.csv` + `/raw_accel_N.csv` song song với
  `session_N.csv`, flush mỗi 500ms để giới hạn mất data nếu board crash giữa chừng.
  → **Ý nghĩa:** ngoài mục tiêu chính (nhận diện hoạt động + đo nhịp tim), dự án còn có 1
  hướng nghiên cứu riêng: so sánh 3 phương pháp lọc nhiễu tín hiệu tim (do cử động tay gây
  ra) để xem cách nào tốt nhất. Muốn so sánh công bằng, cần lưu lại tín hiệu thô (chưa qua
  xử lý gì) chứ không chỉ con số nhịp tim cuối cùng. Tuần này bắt đầu ghi thêm luồng dữ
  liệu thô này song song, không ảnh hưởng luồng dữ liệu chính — đặt nền cho hướng nghiên
  cứu sẽ làm ở các tuần sau (Week 10).

## Kết quả

Pipeline thu thập giờ tự phục hồi (ngưỡng thích nghi), không cần reset thủ công, và bắt
đầu ghi raw waveform — điều kiện cần cho research track LMS/RLS/Wiener sau này.

## Khác biệt so với kế hoạch gốc

Không có model training/quantization tuần này — dataset chưa đủ. Không có PCB order
(thuộc phần Duy, ngoài phạm vi repo này).

---
[← Week 5](week_05.md) · [Weekly reports index](README.md) · [Week 7 →](week_07.md)
