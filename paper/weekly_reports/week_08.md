# Week 8 Report — Dataset scale-up + pipeline automation

Phần việc của **Giang**. Kế hoạch gốc: "Full system integration" (tích hợp firmware +
PCB + enclosure) — phần PCB/enclosure thuộc Duy/Tùng, ngoài phạm vi repo này. Tuần này
tập trung vào chuẩn hoá dataset và tự động hoá pipeline xử lý data.

## Đã làm

- **Raw data cố định trong `experiments/`, dataset xử lý sang `data/processed/`**
  (07-22). Toàn bộ session thu 17/7–20/7 trước đó chỉ tồn tại local, chưa từng commit —
  backup vào git. Từ giờ `experiments/` là raw bất khả xâm phạm; mọi dataset đã lọc phải
  ghi ra `data/processed/` (sinh từ script chạy lại được, không sửa tay).
  → **Ý nghĩa:** đặt ra 1 quy tắc lưu trữ rõ ràng: dữ liệu gốc thu được từ thiết bị (chưa
  qua chỉnh sửa gì) luôn được giữ nguyên vẹn, không ai được sửa tay vào đó — giống như giữ
  bản gốc của 1 tài liệu quan trọng. Mọi bước xử lý/lọc dữ liệu tiếp theo phải được làm
  bằng chương trình có thể chạy lại được, không sửa tay trực tiếp. Điều này đảm bảo nếu
  sau này phát hiện 1 bước xử lý bị sai, có thể chạy lại từ đầu trên dữ liệu gốc thay vì
  dữ liệu đã bị sửa tay không thể phục hồi lại được.
- **Quyết định: giữ transition buffer 15s, không lọc motion-spike tự nhiên** (07-22).
  So sánh chi phí: tăng buffer 15s→20s ăn hết data của các session bị brownout cắt giữa
  chừng — giữ 15s. Outlier check cho thấy 6.34% dòng có "spike" tự nhiên dàn trải đều —
  quyết định giữ nguyên, không lọc, vì model nhắm robust real-world, không phải lab-clean.
  → **Ý nghĩa:** cân nhắc 1 đánh đổi kỹ thuật giữa 2 lựa chọn, có tính toán chứ không đoán
  mò: tăng thời gian đệm giữa các bài tập giúp dữ liệu "sạch" hơn nhưng làm mất luôn dữ
  liệu của những buổi đo bị lỗi mất điện giữa chừng — không đáng đánh đổi. Cũng quyết định
  không lọc bỏ những đoạn dữ liệu "bất thường tự nhiên" (VD: người tham gia cử động bất
  chợt) — vì mục tiêu là AI hoạt động tốt trong đời sống thật (có nhiễu), không phải chỉ
  tốt trên dữ liệu phòng thí nghiệm hoàn hảo.
- **Rule loại session không có activity thật; chia `valid_sessions/` / `firmware_test_fixtures/`**
  (07-22). Phát hiện qua plot: 1 session "running" có accel phẳng tuyệt đối — thiết bị
  nằm yên trên bàn. Mã hoá thành rule tự động (`median(std_mag|running)/median(std_mag|lying) < 3`)
  quét toàn bộ 21 session — 6/21 bị flag, chuyển sang `firmware_test_fixtures/`; 15 session
  còn lại (activity thật) vào `valid_sessions/`, dùng để train.
  → **Ý nghĩa:** phát hiện có những lần "đo" thực ra là lúc test thiết bị (không có ai đeo,
  máy nằm yên trên bàn) bị lẫn vào chung với dữ liệu đo người thật — nếu đưa cả vào train
  AI sẽ dạy sai (dạy rằng "chạy bộ" trông giống "nằm yên"). Viết 1 quy tắc tự động để quét
  và tách riêng loại dữ liệu này ra, đảm bảo chỉ dữ liệu đo người thật mới được dùng để
  huấn luyện AI — 1 bước kiểm soát chất lượng quan trọng, trực tiếp ảnh hưởng độ chính xác
  cuối cùng.
- **Thêm participant log (15 participant) + LOGO-CV check cho hướng fix bug-1** (07-23).
  Test giả thuyết per-axis feature (`mean_ax/ay/az`) trên 4 session có raw accel (P01–P04):
  raw per-axis đạt **68.2%** accuracy (so baseline 48.2%) nhưng P03 rớt còn **46.8%**
  (không hơn baseline); biến thể "relative to own lying baseline" đạt **66.1%**, fix được
  P03 (69.7%) nhưng làm hỏng P01 (45.5%). Chưa đủ N=4 participant để kết luận biến thể nào
  generalize — mở sang tuần sau.
  → **Ý nghĩa:** đây là lúc bắt đầu điều tra 1 vấn đề đã biết từ trước: AI hay nhầm lẫn
  giữa 3 tư thế "nằm/ngồi/đứng" (không nhầm "đi bộ" với "chạy"). Thử 2 cách sửa khác nhau
  và đo kết quả cẩn thận trên từng người tham gia riêng biệt (không chỉ nhìn số trung
  bình) — phát hiện ra: cách sửa nào cũng giúp được người này nhưng lại làm hỏng cho người
  khác, tức là 2 cách thử này chưa phải giải pháp đúng. Đây là bước điều tra khoa học có hệ
  thống (đưa ra giả thuyết → đo → đối chiếu), không phải "thử cho có" — nền tảng để tuần
  sau tìm ra nguyên nhân gốc rễ thật sự (xem Week 9).

## Kết quả

Dataset có quy trình raw/processed rõ ràng, tự động lọc session không hợp lệ. Bug-1
(lying/sitting/standing dễ nhầm) bắt đầu được điều tra có hệ thống thay vì đoán.

## Khác biệt so với kế hoạch gốc

Không có PCB/enclosure integration (thuộc Duy/Tùng). "Full system integration" thực tế
xảy ra muộn hơn nhiều so với kế hoạch — xem Week 11.

---
[← Week 7](week_07.md) · [Weekly reports index](README.md) · [Week 9 →](week_09.md)
