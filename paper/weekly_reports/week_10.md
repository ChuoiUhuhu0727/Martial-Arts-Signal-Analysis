# Week 10 Report — LMS/RLS/Wiener adaptive filter research track (M4, M5)

Phần việc của **Giang**. Kế hoạch gốc: "Web BLE dashboard and final enclosure" — thực tế
tuần này dồn vào research track (LMS/RLS/Wiener), xây từ đầu đến kết quả cuối cùng trong
cùng 1 phiên làm việc (07-28). Matches milestone **M4** (LMS filter) + **M5** (fingertip
vs wrist experiment).

> ⚠️ **KẾT LUẬN CỦA TUẦN NÀY VỀ SAU BỊ BÁC BỎ — xem [Week 13](week_13.md)**
>
> Bốn con số MAE công bố ở tuần này (baseline 26.95 · LMS 26.96 · RLS 29.83 · Wiener 29.96)
> được đo so với nhịp tim suy từ kênh đầu ngón tay. Ngày 15-08, kênh tham chiếu đó bị phát
> hiện **sai gấp đôi ở 3/5 đối tượng** do lỗi octave error, nên cả bốn con số trên đều đo
> bằng một cái thước cong và **không dùng để kết luận được**.
>
> Nội dung tuần này **được giữ nguyên, không sửa lại**. Việc một kết luận tự tin về sau bị
> chính nhóm lật lại là một phần của quá trình nghiên cứu, và là bằng chứng trực tiếp cho
> luận điểm ở Chương 5 mục 5.3 của thesis: các chỉ số đánh giá thông thường không phát hiện
> được lỗi này, vì chúng kiểm tra tính nhất quán chứ không kiểm tra tính đúng đắn vật lý.

## Đã làm

- **`lms_denoise_mvp.py` — MVP đầu tiên (P02, LMS only)** (07-28). Kết quả ban đầu chưa
  dùng được: BPM tức thời nhảy phi thực tế (53→125→133→18.5 bpm liên tiếp lúc nằm yên).
  Quyết định: peak-detection method cần làm lại trước khi so sánh filter nào — không phải
  bug riêng của LMS.
  → **Ý nghĩa:** đây là bước đầu tiên của hướng nghiên cứu riêng (không phải sản phẩm
  chính): tìm hiểu xem thuật toán lọc nhiễu nào giúp đo nhịp tim ở cổ tay chính xác hơn.
  Kết quả thử đầu tiên cho ra những con số vô lý về mặt sinh học (nhịp tim người không thể
  nhảy từ 53 lên 133 rồi xuống 18.5 trong vài giây liên tiếp) — thay vì cố "vá" cho ra số
  đẹp, quyết định dừng lại tìm đúng nguyên nhân gốc: cách nhận diện từng nhịp tim (bước đo
  trước khi so sánh thuật toán lọc) chưa đủ tin cậy. Đây là cách làm khoa học đúng đắn:
  không so sánh 3 phương pháp lọc trên 1 phép đo chưa đáng tin.
- **Làm lại peak-detection 3 vòng** (07-28): range-gate vật lý (40-180bpm) → spectral FFT
  → continuity-tracking + burn-in (giới hạn mỗi window trong 25bpm quanh ước lượng trước,
  seed bằng median 5-window). Sau khi sửa: LMS thắng rõ trên P02 (24.0 vs 29.6 bpm MAE).
  → **Ý nghĩa:** thử 3 cách khác nhau để nhận diện đúng từng nhịp tim từ tín hiệu, mỗi
  cách sau khắc phục điểm yếu của cách trước — giống như tinh chỉnh 1 công cụ đo cho đến
  khi nó đủ tin cậy. Sau khi có công cụ đo đáng tin, mới thấy rõ ràng thuật toán lọc LMS
  giúp cải thiện độ chính xác đo nhịp tim trên người thử nghiệm đầu tiên.
- **Mở rộng ra cả 5 participant dual-PPG** (07-28): **P02 không generalize** — pooled MAE
  baseline=26.95 vs LMS=26.96 (gần như hoà). 3/5 participant LMS giúp, 2/5 làm tệ hơn.
  → **Ý nghĩa:** kết quả tốt trên 1 người không có nghĩa đúng cho tất cả mọi người — đây
  chính là lý do phải test trên nhiều người tham gia khác nhau trước khi kết luận, không
  tin vào 1 kết quả đơn lẻ. Khi mở rộng ra 5 người, kết quả không còn nhất quán như lúc chỉ
  test 1 người — 1 phát hiện quan trọng, tránh việc báo cáo sai 1 kết luận chỉ đúng ngẫu
  nhiên cho 1 trường hợp.
- **Thêm RLS, bắt + sửa bug windup số học** (07-28): RLS đầu tiên nổ số hoàn toàn (residual
  std 7e3→2.3e7) — root cause: λ=0.99 khiến ma trận P tăng không giới hạn trong đoạn accel
  gần-phẳng (lying/sitting/standing). Fix: reset P khi trace(P) vượt ngưỡng. Sau fix: pooled
  MAE RLS=29.83bpm — thắng 3/5 participant nhưng thua đậm ở P04 (46.06).
  → **Ý nghĩa:** thử thêm thuật toán lọc thứ 2 (RLS) để so sánh — thuật toán này ban đầu bị
  lỗi tính toán nghiêm trọng (kết quả tính ra sai lệch cả trăm ngàn lần) đúng vào những lúc
  người tham gia đứng/ngồi/nằm yên (ít chuyển động). Tìm ra nguyên nhân và sửa được lỗi
  tính toán này — 1 dạng công việc debug (tìm lỗi) đòi hỏi hiểu sâu cách thuật toán hoạt
  động bên trong, không chỉ chạy code và nhìn kết quả.
- **Thêm Wiener, hoàn tất so sánh 4 nhánh** (07-28). **[Kết quả này về sau bị bác bỏ — xem Week 13]** **Kết quả cuối: baseline=26.95,
  LMS=26.96, RLS=29.83, Wiener=29.96 (bpm, pooled MAE, N=5)** — không thuật toán nào thắng
  rõ ràng, mỗi participant có filter thắng khác nhau. Kết luận trung thực cho pha MVP: chưa
  filter classical nào chứng minh lợi ích nhất quán so với không lọc gì.
  → **Ý nghĩa:** hoàn tất so sánh cả 3 thuật toán lọc với phương án "không lọc gì cả" làm
  đối chứng. Kết quả trung thực: không thuật toán nào chứng minh được luôn luôn tốt hơn
  không lọc gì, trên cả 5 người thử nghiệm. Đây là 1 kết quả nghiên cứu có giá trị thật để
  đưa vào bài báo khoa học (target Q3 journal) — khoa học không phải lúc nào cũng phải "tìm
  ra cách tốt nhất", chứng minh được "cách này chưa đủ tốt, cần cách khác" cũng là đóng góp
  thật, miễn là đo đạc nghiêm túc và trung thực.
- **2 thử nghiệm bounded cuối** (07-28): (1) reference 3-trục riêng thay vì magnitude gộp
  → kết quả TỆ HƠN mọi filter (24 tap overfit trên ~45k mẫu/session) — giữ magnitude. (2)
  Điều tra vì sao P04 làm RLS/Wiener tệ hẳn (46-47bpm) — correlation(wrist, accel) của P04
  cao nhất (-0.72), gợi ý RLS/Wiener "ăn" cả tín hiệu tim thật khi tương quan mạnh — nhưng
  P03 correlation gần tương đương (-0.47) không sập nặng như P04, nên chưa xác nhận được,
  dừng điều tra ở đây.
  → **Ý nghĩa:** thử thêm 2 hướng cải thiện nữa trong giới hạn thời gian cho phép — 1
  hướng chứng minh rõ ràng là không nên làm (làm mọi thứ tệ hơn), hướng còn lại có manh mối
  hợp lý nhưng chưa đủ bằng chứng để kết luận chắc chắn. Chủ động dừng lại đúng lúc thay vì
  tiếp tục đào sâu vô thời hạn khi chưa có lý do mới — 1 kỹ năng quản lý thời gian nghiên
  cứu quan trọng không kém kỹ năng kỹ thuật.

## Kết quả

**Không filter nào thắng nhất quán ở N=5** — đây là kết quả nghiên cứu thật (research
question trả lời được: "không", có giá trị publish), không phải thất bại pipeline.

## Khác biệt so với kế hoạch gốc

Không có Web BLE dashboard tuần này (chưa làm — xem ghi chú Week 13). Enclosure thuộc
Tùng, ngoài phạm vi repo này.

---
[← Week 9](week_09.md) · [Weekly reports index](README.md) · [Week 11 →](week_11.md)

**Dẫn tới chương nào của thesis:** Chương 4 mục 4.1–4.2 (thiết kế thí nghiệm và kết quả vòng đầu). Kết luận của tuần này bị lật ở mục 4.3–4.6.
