# Báo cáo hàng tuần — Tuần 5 đến Tuần 10

Báo cáo **đã làm gì / kết quả gì** (không phải kế hoạch), tổng hợp từ git commit history +
`CHANGELOG.md` + `README.md` Progress Log.

**Cách chia tuần:** git log thực tế cho thấy công việc dồn vào khoảng 6 tuần calendar
(27/6 → 20/8). Nội dung được **nén theo chủ đề logic** thành 6 báo cáo, mỗi báo cáo là một
giai đoạn công việc mạch lạc, thay vì cắt theo ngày tháng. Tuần 9 gộp toàn bộ phần phân
loại hoạt động từ lúc huấn luyện đến lúc chạy trên thiết bị; Tuần 10 gộp hướng nghiên cứu
lọc nhiễu và phát hiện lật ngược nó.

## Quan hệ với thesis

Hai tài liệu này **bổ sung nhau chứ không thay thế nhau**:

- **Thesis** (`../THESIS.md`) tổ chức theo **lập luận**: vấn đề → nguyên nhân gốc → giải
  pháp. Nó cho biết *kết luận cuối cùng là gì*.
- **Weekly reports** tổ chức theo **thời gian**: tuần này làm được gì. Chúng cho biết
  *kết luận đã thay đổi thế nào theo thời gian* — điều mà thesis không thể tự chứng minh về
  chính nó, vì thesis được viết sau khi đã biết đáp án.

Ví dụ rõ nhất nằm ngay trong [Week 10](week_10.md): phần 1 công bố kết quả so sánh ba bộ
lọc với sự tự tin, rồi phần 3 lật lại chính kết quả đó sau khi phát hiện thước đo tham chiếu
bị hỏng. Trình tự đó **được giữ nguyên, không sắp xếp lại cho gọn** — quá trình tự phát hiện
và sửa sai là một phần của kết quả nghiên cứu.

| Tuần | Chủ đề | Milestone | Dẫn tới chương nào của thesis |
| :--- | :--- | :--- | :--- |
| [Week 5](week_05.md) | Dựng nền móng thu thập dữ liệu | — | Ch. 2.1 — kiến trúc thiết bị và firmware |
| [Week 6](week_06.md) | Làm chắc quy trình thu dữ liệu | — | Ch. 2.1, 2.2 — giao thức thu |
| [Week 7](week_07.md) | Gắn cảm biến thứ hai làm đáp án đối chiếu | — | Ch. 2.2, 4.1 — kênh tham chiếu |
| [Week 8](week_08.md) | Kiểm soát chất lượng, phát hiện 6 buổi đo giả | — | Ch. 2.2 — bộ dữ liệu; Ch. 5.3 |
| [Week 9](week_09.md) | Từ mô hình đầu tiên đến AI chạy trên thiết bị | M3, M6 | Ch. 3.2–3.5, Ch. 5.1 |
| [Week 10](week_10.md) | Nghiên cứu lọc nhiễu, và phát hiện lật ngược nó | M4, M5 | Ch. 4 toàn bộ, Ch. 5.3–5.4 |

Tuần 1–4: đã nộp report riêng trước đó, không nằm trong thư mục này.
