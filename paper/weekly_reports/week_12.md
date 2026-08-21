# Week 12 Report — Chốt bộ dữ liệu và tìm ra cách định nghĩa lại bài toán

## Tuần này làm gì — nhìn tổng quan

**Giai đoạn:** Phase 3 — *Polish and Documentation* (Tuần 10–13).

**Một câu tóm tắt:** chốt bộ dữ liệu cuối cùng ở **18 người tham gia**, và tìm ra rằng chỉ
cần **định nghĩa lại bài toán cho khớp với năng lực của cảm biến** là độ chính xác nhảy từ
54.8% lên **85.3%**.

**Ý nghĩa trong tổng thể:** đây là hệ quả trực tiếp của phát hiện ở Tuần 9. Khi đã biết
bộ cảm biến hiện tại *về nguyên lý không thể* phân biệt ba tư thế tĩnh, thì giải pháp đúng
không phải là chỉnh mô hình thêm — mà là **hỏi lại xem bài toán có đang được đặt đúng
không**.

---

## Nhóm việc 1 — Chốt bộ dữ liệu

- **Thêm người tham gia thứ 18**, khác với buổi đo thử nghiệm đã bị loại ở Tuần 11.
  → Bộ dữ liệu cuối cùng: **18 người**.

## Nhóm việc 2 — Gộp ba tư thế tĩnh thành một nhóm

![Hình 12.1: Ba tư thế tĩnh được gộp thành một nhóm "nghỉ". Đây không phải chọn cách chia nào ra số đẹp hơn, mà là định nghĩa lại bài toán cho khớp với thứ cảm biến đo được.](figures/week12_regroup.png)

- **Giữ nguyên tuyệt đối mọi thứ khác, chỉ đổi cách gộp nhãn** (~07-30): cùng mô hình, cùng
  bốn đặc trưng, cùng bộ dữ liệu, cùng cách chấm điểm. Chỉ gộp nằm / ngồi / đứng thành một
  nhóm "nghỉ".

| Bài toán | Độ chính xác | Nhận đúng nhóm "nghỉ" |
| :--- | ---: | ---: |
| 5 lớp | 54.8% | — |
| **3 lớp** | **85.3%** | **95.1%** |

### Gộp lớp như vậy có phải là chọn cách chia ra số đẹp không?

Đây là câu hỏi quan trọng nhất phải trả lời, vì nhìn từ ngoài rất giống việc "thử nhiều
cách chia rồi giữ cách nào cho điểm cao nhất".

**Không phải**, vì hai lý do:

1. **Ranh giới gộp được suy ra trước khi nhìn kết quả**, từ nguyên nhân gốc đã chứng minh ở
   Tuần 9: cả bốn đặc trưng đều là hàm của độ lớn gia tốc, mà độ lớn thì không đổi khi cổ
   tay xoay. Ba tư thế tĩnh khác nhau đúng ở chỗ đó. Đây là giới hạn **cấu trúc** của bộ
   đặc trưng, không phải chuyện may rủi.
2. **Việc gộp loại bỏ đúng phần mà bộ đặc trưng không quan sát được**, và giữ nguyên phần
   nó quan sát được rất tốt — khác biệt về cường độ chuyển động giữa nghỉ, đi bộ và chạy.

→ **Ý nghĩa:** bước nhảy 54.8% → 85.3% phản ánh việc **loại bỏ một giới hạn đã hiểu rõ
nguyên nhân**, không phải một phép thử may mắn.

**Điều này không tuyên bố:** việc gộp lớp **không** làm mô hình phân biệt được nằm, ngồi,
đứng. Thông tin đó vẫn mất. Chỉ là bài toán đã được định nghĩa lại cho đúng với năng lực đo
thật của phần cứng hiện tại.

## Nhóm việc 3 — Quyết định báo cáo cả hai con số

- **Giữ bản 5 lớp làm số chính, bản 3 lớp là kết quả đi kèm** (~07-30).
  → **Ý nghĩa:** bản 5 lớp tuy kém chính xác hơn nhưng vẫn giữ được thông tin về ba tư thế
  tĩnh, có giá trị thực tế hơn cho ứng dụng cuối. Báo cáo cả hai, kèm giải thích, thay vì
  chỉ chọn con số đẹp hơn để trưng ra.

- **Dựng khung sườn hai bản báo cáo** cho hai hướng của dự án, làm nguyên liệu cho Tuần 13.

---

## Kết quả cuối tuần

| Hạng mục | Kết quả |
| :--- | :--- |
| Bộ dữ liệu cuối cùng | 18 người tham gia |
| Con số chính | 5 lớp — 54.8% |
| Kết quả đi kèm | 3 lớp — 85.3% |

## Khác biệt so với kế hoạch gốc

Kế hoạch gốc ghi *"External user testing and final iteration"* — thử nghiệm với người hoàn
toàn ngoài dự án. Chưa làm được: toàn bộ người tham gia hiện tại đều là người quen biết
trong hoặc gần nhóm.

**Dẫn tới chương nào của thesis:** Chương 3 mục 3.5 (tái thiết kế bài toán và đánh giá công
bằng so với mốc cơ sở).

---
[← Week 11](week_11.md) · [Weekly reports index](README.md) · [Week 13 →](week_13.md)
