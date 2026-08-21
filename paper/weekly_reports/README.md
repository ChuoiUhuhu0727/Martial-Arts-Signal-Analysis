# Weekly Reports — Week 5 → Week 13 (Giang's part)

Báo cáo **đã làm gì / kết quả gì** (không phải kế hoạch), tổng hợp từ git commit history +
`CHANGELOG.md` + `README.md` Progress Log. Chỉ có phần việc của Giang — Duy/Tùng không có
trong repo này.

**Cách chia tuần:** git log thực tế cho thấy công việc dồn vào ~6 tuần calendar thật
(27/6 → 20/8), không trải đều 9 tuần như lịch gốc (30/6 → 1/9). Theo lựa chọn của Giang,
nội dung được **nén theo thứ tự/chủ đề logic**, bám sát chủ đề gốc của từng tuần trong
[`../../archived/project_description.md`](../../archived/project_description.md) nhất
có thể — không đối chiếu ngày tháng thật theo từng tuần.

## Quan hệ với thesis

Hai tài liệu này **bổ sung nhau chứ không thay thế nhau**:

- **Thesis** (`../THESIS.md`) tổ chức theo **lập luận**: vấn đề → nguyên nhân gốc → giải
  pháp. Nó cho biết *kết luận cuối cùng là gì*.
- **Weekly reports** tổ chức theo **thời gian**: tuần này làm được gì. Chúng cho biết
  *kết luận đã thay đổi thế nào theo thời gian* — điều mà thesis không thể tự chứng minh về
  chính nó, vì thesis được viết sau khi đã biết đáp án.

Ví dụ rõ nhất: [Week 10](week_10.md) công bố kết quả so sánh 3 bộ lọc với sự tự tin, rồi
[Week 13](week_13.md) lật lại chính kết quả đó sau khi phát hiện thước đo tham chiếu bị
hỏng. Nội dung Week 10 **được giữ nguyên, không sửa lại cho khớp thesis** — quá trình tự
phát hiện và sửa sai là một phần của kết quả nghiên cứu.

| Tuần | Chủ đề | Milestone | Dẫn tới chương nào của thesis |
| :--- | :--- | :--- | :--- |
| [Week 5](week_05.md) | Firmware & BLE data-collection foundation | — | Ch. 2.1 — kiến trúc thiết bị và firmware |
| [Week 6](week_06.md) | Data-collection pipeline hardening | — | Ch. 2.1, 2.2 — giao thức thu |
| [Week 7](week_07.md) | Second PPG channel + dataset quality rules | — | Ch. 2.2, 4.1 — kênh tham chiếu |
| [Week 8](week_08.md) | Dataset scale-up + pipeline automation | — | Ch. 2.2 — bộ dữ liệu |
| [Week 9](week_09.md) | Pipeline automation, bug-1 closed, classifier trained | M3 | Ch. 3.2–3.4 — kết quả 5 lớp và nguyên nhân gốc |
| [Week 10](week_10.md) | LMS/RLS/Wiener adaptive filter research track | M4, M5 | Ch. 4.1–4.2 — **kết luận bị lật ở 4.3–4.6** |
| [Week 11](week_11.md) | Firmware integration + hardware validation | M6 | Ch. 2.1, 5.1 — kiến trúc tích hợp |
| [Week 12](week_12.md) | Dataset finalized (N=18), 3-class secondary finding | — | Ch. 3.5 — tái thiết kế 3 lớp |
| [Week 13](week_13.md) | **Viết report, và phát hiện lật ngược Subsystem B** | — | Ch. 4.3–4.6, 5.3, 5.4 |

Tuần 1–4: đã nộp report riêng trước đó, không nằm trong thư mục này.
