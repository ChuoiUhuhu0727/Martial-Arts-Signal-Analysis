# Week 7 Report — Second PPG channel + dataset quality rules

Phần việc của **Giang**. Kế hoạch gốc: "adaptive PPG peak detection, LMS filter, đo BPM
error wrist vs fingertip" — hạ tầng cho thí nghiệm này được dựng tuần này; kết quả đo
thật của LMS/RLS/Wiener đến sau khi đủ data (xem Week 10).

## Đã làm

- **Thêm MAX30102 thứ 2 (fingertip, ground-truth channel)** (07-16). Cảm biến có địa chỉ
  I2C cố định (0x57) nên không dùng chung bus được — con mới đi trên bus I2C riêng
  (`Wire1`), task riêng `task_ppg2_reader`. Chỉ ghi raw vào `/raw_ppg2_N.csv`, không đưa
  vào BPM sống — vai trò là tham chiếu ground-truth cho so sánh LMS/RLS/Wiener sau này.
  → **Ý nghĩa:** để biết phương pháp lọc nhiễu nào đo nhịp tim chính xác nhất, cần có 1
  "đáp án đúng" để so sánh. Đo nhịp tim ở đầu ngón tay (ít bị nhiễu do cử động) cho kết
  quả sạch và đáng tin hơn nhiều so với đo ở cổ tay — nên gắn thêm 1 cảm biến thứ 2 ở đầu
  ngón tay, chạy song song với cảm biến chính ở cổ tay, chỉ để làm "đáp án tham chiếu",
  không phải số liệu hiển thị cho người dùng cuối. Đây là thiết bị đo dùng riêng cho mục
  đích nghiên cứu, không phải tính năng của sản phẩm.
- **Custom partition table cho `firmware_ble`** (07-17). Partition mặc định chỉ cấp
  1.5MB LittleFS (profile 4MB chip dù board thật có 8MB) — không đủ chứa raw waveform 1
  participant đủ 5 hoạt động (~1.6MB). Đổi sang `partitions_ble_8mb.csv` (app0 3MB +
  spiffs 4.94MB).
  → **Ý nghĩa:** bộ nhớ lưu trữ trong thiết bị mặc định chỉ được cấp phát 1 phần nhỏ hơn
  nhiều so với dung lượng thật của chip — không đủ chứa hết dữ liệu thô của 1 người đo đủ
  5 hoạt động. Chỉnh lại cấu hình để dùng đúng hết dung lượng bộ nhớ sẵn có trên phần
  cứng. Nếu không sửa, dữ liệu của 1 buổi đo có thể bị cắt cụt giữa chừng vì hết chỗ lưu.
- **Known limitation ghi nhận: `raw_ppg_N.csv` mất ~28% mẫu** (07-17). Đo trên 1 dry-run
  8 phút: raw waveform 100Hz chỉ giữ ~72% mẫu kỳ vọng — nghi do flush flash mỗi 500ms làm
  khựng hệ thống ngắn. `session_N.csv` (dataset chính, không phải raw) không bị ảnh
  hưởng, vẫn 100% đầy đủ. Replay thuật toán onset/reset trên raw thật: chỉ 58/228 wave
  được accept làm beat — xác nhận `bpm` live chỉ nên coi là chỉ báo thô, ground truth thật
  phải tính offline từ raw waveform.
  → **Ý nghĩa:** đo và ghi nhận trung thực 1 giới hạn kỹ thuật: khi ghi dữ liệu thô tốc độ
  cao, thiết bị bị mất khoảng 28% số mẫu do phải dừng lại lưu vào bộ nhớ định kỳ. Quan
  trọng: đây chỉ ảnh hưởng luồng dữ liệu thô phụ trợ cho nghiên cứu (Week 6, Week 10),
  KHÔNG ảnh hưởng dữ liệu chính dùng để nhận diện hoạt động (vẫn nguyên vẹn 100%). Ghi
  nhận rõ giới hạn này để không hiểu nhầm số nhịp tim hiển thị trực tiếp là số liệu chính
  xác tuyệt đối — số chính xác phải tính lại sau từ dữ liệu thô, không phải số hiện ngay
  lúc đo.
- **Known issue ghi nhận: BLE disconnect dù đứng sát laptop** (07-17). Không ảnh hưởng
  data (kiến trúc flash-trước-BLE-sau) — để fix sau, không chặn việc thu data tiếp.
  → **Ý nghĩa:** ghi nhận 1 lỗi kết nối Bluetooth chưa rõ nguyên nhân, nhưng nhờ quyết
  định nền tảng ở Week 5 (luôn lưu vào bộ nhớ trong trước), lỗi này không làm mất dữ liệu
  nào — chỉ ảnh hưởng phần xem trực tiếp. Quyết định gác lại, không dừng việc thu data để
  sửa lỗi không ảnh hưởng kết quả.

## Kết quả

2 kênh PPG song song (wrist + fingertip) hoạt động, đủ dung lượng flash cho raw capture
đầy đủ 1 participant. Giới hạn đã biết: raw waveform mất mẫu ~28% (ảnh hưởng research
track LMS, không ảnh hưởng dataset chính dùng để train classifier).

## Khác biệt so với kế hoạch gốc

Chưa đo BPM error thật (cần data từ nhiều participant trước) — đây là bước dựng hạ tầng
đo, không phải kết quả đo.

---
[← Week 6](week_06.md) · [Weekly reports index](README.md) · [Week 8 →](week_08.md)
