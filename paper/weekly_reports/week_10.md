# Week 10 Report — Hướng nghiên cứu lọc nhiễu, và phát hiện lật ngược chính nó

## Tuần này làm gì — nhìn tổng quan

**Giai đoạn:** Phase 3 — *Polish and Documentation*, tuần cuối của dự án. Khớp với mốc
**M4** và **M5**.

**Một câu tóm tắt:** dựng và chạy trọn vẹn hướng nghiên cứu riêng — so sánh ba thuật toán
lọc nhiễu — rồi **trong lúc viết báo cáo tổng kết thì phát hiện cái thước dùng để chấm điểm
chúng bị sai gấp đôi**, buộc phải bác bỏ và làm lại toàn bộ.

**Ý nghĩa trong tổng thể:** đây là tuần quan trọng nhất của cả dự án. Không phải vì làm
thêm được tính năng gì, mà vì phát hiện ra một kết quả tưởng đã xong thực ra không dùng
được — và kịp sửa trước khi nộp.

> **Vì sao lỗi lộ ra đúng lúc viết báo cáo?** Vì viết buộc phải giải thích từng con số cho
> người khác hiểu. Mà muốn giải thích được thì phải tự hỏi *con số này đến từ đâu, và nó có
> hợp lý không* — câu hỏi mà suốt các tuần trước không ai đặt ra, vì mọi thứ đang chạy trơn
> tru.

---

## Phần 1 — Bố trí thí nghiệm so sánh ba thuật toán

![Hình 10.1: Tín hiệu ở cổ tay lẫn nhiễu do cử động tay. Cả ba thuật toán đều dùng cảm biến chuyển động để đoán phần nhiễu rồi trừ đi, sau đó so kết quả với nhịp tim đo ở đầu ngón tay.](figures/week10_filter_setup.png)

Cả ba thuật toán dựa trên cùng một ý tưởng: **tín hiệu ở cổ tay = nhịp tim thật + nhiễu do
cử động**. Dùng cảm biến chuyển động để đoán phần nhiễu, rồi trừ đi. Chúng chỉ khác nhau ở
cách đoán.

- **Lần thử đầu cho kết quả vô lý về mặt sinh học** (07-28): nhịp tim nhảy 53 → 125 → 133 →
  18.5 trong vài giây, trong khi người tham gia đang **nằm yên**.
  → **Ý nghĩa:** thay vì cố chỉnh cho ra số đẹp, quyết định dừng lại. Nguyên nhân không nằm
  ở thuật toán lọc mà ở **bước đo nhịp tim** đứng trước nó.

- **Làm lại cách nhận diện nhịp tim qua ba vòng** (07-28), mỗi vòng khắc phục điểm yếu của
  vòng trước.
  → *(Ghi chú muộn: chính vòng sửa thứ ba — thêm ràng buộc không cho nhịp tim nhảy quá xa
  giữa hai lần đo — về sau hoá ra là thứ che giấu lỗi lớn nhất của dự án. Xem Phần 3.)*

- **Mở rộng ra 5 người: kết quả tốt trên một người không giữ được** (07-28). Ba người được
  cải thiện, hai người tệ đi.

- **Thêm thuật toán thứ hai, bắt được lỗi tính toán nghiêm trọng** (07-28). RLS ban đầu cho
  kết quả sai lệch hàng trăm nghìn lần, đúng vào lúc người tham gia **đứng, ngồi hoặc nằm
  yên**. Dạng lỗi này phải hiểu thuật toán bên trong mới thấy: khi gần như không có chuyển
  động, một đại lượng nội bộ phình to không giới hạn.

- **Thêm thuật toán thứ ba, hoàn tất so sánh bốn nhánh** (07-28).

| Cách xử lý | Sai số trung bình *(số này về sau bị bác bỏ)* |
| :--- | ---: |
| Không lọc gì | 26.95 |
| NLMS | 26.96 |
| RLS | 29.83 |
| Wiener | 29.96 |

- **Hai thử nghiệm cuối** (07-28): dùng ba trục cảm biến riêng thay vì gộp — **tệ hơn ở mọi
  thuật toán**; điều tra vì sao một người làm hai thuật toán tệ hẳn — có manh mối nhưng
  **chưa đủ bằng chứng**, chủ động dừng thay vì đào sâu vô thời hạn.

## Phần 2 — Sửa một lỗi so sánh trên sai tập dữ liệu (14-08)

- **Mốc cơ sở được tính trên toàn bộ 20.258 dòng**, trong khi mô hình được huấn luyện và
  chấm điểm trên 16.880 dòng đã lọc bỏ đoạn chuyển tiếp. Hai con số đem so với nhau nhưng
  mô tả hai tập dữ liệu khác nhau.
  → **Ý nghĩa:** kết luận không đổi, nhưng đây là dạng lỗi người phản biện bắt ngay: so
  sánh hai con số đo trên hai tập dữ liệu khác nhau.

## Phần 3 — Bác bỏ thước đo và làm lại toàn bộ (15-08)

- **Phép thử sinh lý học trên kênh tham chiếu.** Câu hỏi rẻ nhất có thể đặt: *nhịp tim lúc
  chạy có cao hơn lúc nằm không?* Kết quả: kênh đầu ngón tay **trượt ở 3/5 người**. Nặng
  nhất: một người ghi nhận đứng yên 127.7 nhịp/phút nhưng chạy chỉ 89.7.

- **Vẽ dạng sóng thô ra và đếm đỉnh bằng mắt** để phân định: cảm biến hỏng hay thuật toán
  hỏng? Dạng sóng **rất sạch** — 30 đỉnh trong 12 giây, tức 155.6 nhịp/phút. Thuật toán báo
  77.0, **đúng một nửa**. → Cảm biến không hỏng, thuật toán hỏng.

- **Loại trừ cách giải thích cạnh tranh.** Nếu mỗi nhịp bị đếm thành hai đỉnh thì khoảng
  cách giữa các đỉnh phải so le dài-ngắn. Đo được: tỉ lệ khoảng lẻ/chẵn = **1.03** (đều tăm
  tắp), tỉ lệ biên độ lẻ/chẵn = **2.22**. Vậy thứ so le là **biên độ**, không phải khoảng
  cách.

![Hình 10.2: Sóng nhịp tim khi chạy có đỉnh cao và đỉnh thấp xen kẽ. Máy chỉ đếm những đỉnh cao, nên báo đúng một nửa nhịp thật.](figures/week13_octave_error.png)

- **Bộ ước lượng mới.** Đo trung vị khoảng cách đỉnh trong miền thời gian, trả về "không đọc
  được" khi nhịp quá không đều thay vì đoán bừa, bỏ hoàn toàn ràng buộc liên tục.

- **Kiểm chứng ngược bằng đếm tay:** một ca từ 77.0 → **156.9** (đếm tay 155.6); ca khác từ
  155.8 → **118.9** (đếm tay 111.3). Số người qua kiểm tra sinh lý tăng từ **2/5 lên 4/5**.

- **Chạy lại toàn bộ so sánh**, giữ nguyên vẹn cả ba thuật toán, số tham số và tín hiệu tham
  chiếu — chỉ đổi cách đọc nhịp tim ra khỏi dạng sóng.

### Vì sao lỗi này sống sót nhiều tuần?

![Hình 10.3: Lỗi nằm ở tầng đo, nhưng bộ chặn lại nằm ở tầng làm mượt — nên khi tầng đo thỉnh thoảng bắt đúng, tầng làm mượt lại gạt đi.](figures/week13_two_layers.png)

Pipeline nhịp tim có hai tầng riêng biệt. **Tầng đo** đọc 8 giây sóng và trả ra một con số.
**Tầng làm mượt** nhận dãy số theo thời gian và loại bỏ bước nhảy phi lý — ràng buộc thêm ở
Phần 1 nằm ở tầng này.

Lỗi phát sinh ở **tầng đo**. Khi tầng này liên tục trả ra dãy [77, 77, 77, …] cực kỳ nhất
quán, tầng làm mượt tin tưởng hoàn toàn. Tệ hơn: khi tầng đo thỉnh thoảng bắt đúng 156, tầng
làm mượt **gạt đi** vì cho rằng nhịp tim không thể nhảy nhiều đến thế. **Hệ thống đã chủ
động bảo vệ con số sai.**

**Bài học kiến trúc:** bộ làm mượt chỉ khử được *nhiễu ngẫu nhiên*, không khử được *sai số
hệ thống*. Gặp sai số hệ thống, nó bám theo giá trị sai một cách êm ái và khiến con số sai
trông đáng tin hơn cả trước khi lọc. Đây cũng là lý do một bộ lọc Kalman — thứ trực giác đầu
tiên nghĩ tới — **sẽ không sửa được bug này**: nó nằm sai tầng.

## Phần 4 — Kết quả thật sau khi sửa, và tổng kết

| Tín hiệu | Tỉ lệ cửa sổ đọc được nhịp tim |
| :--- | ---: |
| Đầu ngón tay (tham chiếu) | 35.0% |
| Cổ tay, không lọc | **9.6%** |
| Cổ tay + NLMS | 8.0% |
| Cổ tay + RLS | 5.5% |
| Cổ tay + Wiener | 12.7% |

Kết luận không phụ thuộc vào ngưỡng đã chọn: siết chặt tiêu chí thì khoảng cách giữa hai
kênh giãn tới **12.2 lần**.

→ **Ý nghĩa:** câu hỏi nghiên cứu của proposal — *"thuật toán nào tốt nhất"* — **đặt sai
tiền đề**. Trong khoảng 90% thời gian, tín hiệu cổ tay ở cấu hình phần cứng này không chứa
nhịp đập nào để mà khử nhiễu. Bộ lọc *tách* tín hiệu khỏi nhiễu, nó không *tạo ra* tín hiệu.
Nguyên nhân nằm ở **bước sóng quang học** — tức tầng thu tín hiệu, không phải tầng thuật
toán.

- **Đối chiếu proposal** (15-08): rà 14 hạng mục cam kết với kết quả thật, kèm lý do cho
  từng chỗ đổi hướng.
- **Gộp hai báo cáo thành thesis 7 chương** (20-08), kèm bản tiếng Anh.

## Nhìn lại: một dạng lỗi lặp lại ba lần

| Lần | Cái được tin | Thực tế | Phát hiện bằng |
| :--- | :--- | :--- | :--- |
| Tuần 8 | 6 buổi đo "đủ nhãn, đủ dòng, log sạch" | Thiết bị nằm im trên bàn, không ai đeo | Vẽ dạng sóng thô ra nhìn |
| Tuần 9 | 4 đặc trưng đủ để phân biệt 5 lớp | Độ lớn bất biến với phép xoay, xoá mất hướng | Lập luận toán học ba dòng |
| Tuần 10 | Đầu ngón tay là chuẩn đối chiếu sạch | Sai gấp đôi ở 3/5 người | Hỏi "chạy có cao hơn nằm không?" |

Cả ba phép thử phát hiện ra lỗi đều tốn **dưới 15 phút**, và cả ba đều nằm **ngoài** mọi quy
trình đánh giá tự động. Lý do: các chỉ số kiểm tra dữ liệu *có ăn khớp với nhau không*, chứ
không kiểm tra dữ liệu *có đúng với thực tế vật lý không*.

---

## Kết quả cuối dự án

Một thesis 7 chương (31 trang, bản Việt và Anh), một tài liệu đối chiếu proposal, năm script
mới, mười một hình. Kết quả của phân hệ nhịp tim là một **kết quả âm tính đã được kiểm chứng
chặt chẽ**: bộ lọc phần mềm không bù đắp được cho lựa chọn sai bước sóng ở tầng phần cứng.

## Khác biệt so với kế hoạch gốc

Chưa có: bảng điều khiển web, video demo, kiểm tra chạy liên tục 60 phút. Phần tài liệu thì
vượt kế hoạch — thay vì một bài viết 1.000–1.500 từ, đã ra một thesis hoàn chỉnh kèm bản
tiếng Anh.

**Dẫn tới chương nào của thesis:** Chương 4 toàn bộ, Chương 5 mục 5.3 và 5.4.

---
[← Week 9](week_09.md) · [Weekly reports index](README.md)
