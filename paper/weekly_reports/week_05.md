# Week 5 Report — Firmware & BLE data-collection foundation

Phần việc của **Giang** (Duy/Tùng không có trong repo này). Kế hoạch gốc tuần này:
"TFLite Micro setup and Gerber files" — thực tế phần Giang lệch khỏi TFLite Micro ngay từ
đầu (lý do: xem Week 9), tuần này thực chất là dựng nền móng thu thập data qua BLE
(Bluetooth) — bước bắt buộc phải xong trước khi có gì để đưa vào AI, vì không có dữ liệu
đáng tin thì không train được model.

## Đã làm

- **Kiến trúc: flash là nguồn sự thật, wireless chỉ best-effort** (07-07). Mọi row ghi
  vào LittleFS vô điều kiện; WiFi/BLE chỉ dùng để xem live. Lý do: radio contention
  (WiFi+BLE chung ăng-ten, WiFi campus nghẽn) khiến wireless-là-primary không đáng tin.
  → **Ý nghĩa:** quyết định dữ liệu thu được sẽ được lưu thẳng vào bộ nhớ trong của
  thiết bị (giống ghi vào ổ cứng riêng) trước, còn tín hiệu Bluetooth chỉ để xem trực
  tiếp cho biết chứ không phải nơi lưu chính. Vì Bluetooth thỉnh thoảng mất sóng — nếu
  lỡ dựa hẳn vào nó để lưu, một lần mất sóng giữa buổi đo là mất luôn dữ liệu của người
  tham gia hôm đó (không đo lại được, vì mỗi người chỉ đến 1 lần). Đây là quyết định nền
  tảng bảo vệ toàn bộ dữ liệu sẽ thu trong các tuần sau.
- **Đổi nguồn điện: power bank thường → pin LiPo qua JST** (07-07). Power bank thường tự
  ngắt sau ~30s vì ESP32 không rút đủ dòng — cắt session giữa chừng không báo lỗi.
  → **Ý nghĩa:** đổi loại pin cấp điện cho thiết bị. Pin sạc dự phòng thông thường (như
  sạc điện thoại) tự tắt sau 30 giây vì "tưởng" thiết bị nhỏ này không cắm gì — làm thiết
  bị tắt đột ngột giữa lúc đang đo người tham gia. Đổi sang loại pin chuyên dụng cắm
  thẳng để tránh việc này lặp lại, đảm bảo mỗi buổi đo chạy trọn vẹn không bị ngắt giữa
  chừng.
- **Pivot transport: BLE thay WiFi/Jetson AP làm nhánh chính** (07-10, `firmware_ble/`).
  `firmware_main/` (Jetson WiFi AP + UDP) parked, không xoá — debug NetworkManager tốn
  quá nhiều thời gian; ưu tiên độ ổn định đã chứng minh hơn tính năng mới.
  → **Ý nghĩa:** ban đầu định truyền dữ liệu qua WiFi thông qua 1 máy tính trung gian
  (Jetson), nhưng gặp lỗi phần mềm mạng khó sửa, tốn nhiều thời gian mà chưa chắc xong.
  Quyết định chuyển hẳn sang Bluetooth (kết nối trực tiếp thiết bị — máy tính, không qua
  máy trung gian) vì đã chứng minh chạy ổn định. Đây là quyết định đánh đổi kỹ thuật: bỏ
  phương án mới rủi ro cao để chọn phương án chắc chắn chạy được, tránh trễ tiến độ thu
  dữ liệu — không giữ nguyên cả 2 hướng cùng lúc sẽ lãng phí thời gian.
- **BLE payload embed full row schema** (07-10) — device là nguồn sự thật duy nhất cho
  cả flash lẫn BLE, tránh lệch giờ (dual-clock-drift) giữa `log_ble.py` và thiết bị.
  → **Ý nghĩa:** gói tin gửi qua Bluetooth giờ do chính thiết bị tạo ra đầy đủ thông tin
  (nhãn hoạt động, mốc thời gian...), thay vì để máy tính nhận tự đoán lại — tránh trường
  hợp đồng hồ của thiết bị và đồng hồ của máy tính lệch nhau vài giây làm sai lệch dữ liệu
  đã gắn nhãn.
- **Fix: BLE advertising không tự resume sau disconnect** (07-10) — thêm callback
  `onDisconnect()` + watchdog 5s; `log_ble.py` re-scan mỗi lần reconnect.
  → **Ý nghĩa:** sửa lỗi thiết bị không tự "phát tín hiệu tìm kết nối lại" sau khi bị rớt
  kết nối Bluetooth — trước đó phải tắt-mở lại tay. Sau khi sửa, thiết bị tự phục hồi,
  giảm số lần phải can thiệp thủ công giữa lúc đang đo người tham gia.
- **`visualize_session.py`** (07-10) — validate data bằng mắt trước khi push, dựa trên
  assumption cường độ vận động tăng dần lying→sitting→standing→walking→running.
  → **Ý nghĩa:** viết công cụ vẽ biểu đồ để kiểm tra bằng mắt xem 1 lần đo có "hợp lý"
  không (ví dụ: lúc đi bộ máy phải rung nhiều hơn lúc nằm yên) trước khi đưa dữ liệu đó
  vào huấn luyện AI. Đây là bước kiểm tra chất lượng, giúp phát hiện sớm lần đo bị lỗi
  thay vì để đến khi train model mới phát hiện ra dữ liệu sai.
- **BLE payload thêm `ppgOK` + `seconds_left`** (07-10) — 2 field tính ở phía device để
  live-view cảnh báo sensor lệch + đếm ngược chính xác.
  → **Ý nghĩa:** thêm 2 thông tin hiển thị ngay trong lúc đang đo: cảm biến có đang áp
  đúng vị trí trên da không, và còn bao nhiêu giây nữa hết bài tập hiện tại. Giúp người
  vận hành (Giang) biết ngay tại chỗ nếu cảm biến bị lệch để chỉnh lại kịp thời, thay vì
  phát hiện sau khi buổi đo đã kết thúc và dữ liệu đã hỏng không cứu được.
- **`TEAMMATE_SETUP.md`: thêm đường dẫn không cần Git** (07-11) — teammate tải/nộp data
  qua giao diện web GitHub (ZIP download + upload trực tiếp).
  → **Ý nghĩa:** viết hướng dẫn để đồng đội không rành lập trình vẫn nộp được dữ liệu qua
  giao diện web thông thường, không cần cài công cụ lập trình phức tạp. Giúp cả nhóm cùng
  tham gia thu thập dữ liệu, không bị giới hạn ở việc ai biết dùng công cụ chuyên môn.

## Khác biệt so với kế hoạch gốc

Kế hoạch gốc ghi TFLite Micro + Gerber files (PCB, thuộc phần Duy). Thực tế phần Giang
tuần này không đụng tới model/AI — toàn bộ là hạ tầng thu thập data ổn định qua BLE,
vì đây là điều kiện tiên quyết: không có data đáng tin thì chưa train được gì.

---
[Weekly reports index](README.md) · [Week 6 →](week_06.md)
