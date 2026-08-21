# Prototype Testing Demonstration 2

**Thiết bị đeo cổ tay nhận diện hoạt động và đo nhịp tim — Báo cáo kiểm thử nguyên mẫu**

Wearable Activity & Health Monitor · Subsystem: Firmware & AI

---

## 1. Nguyên mẫu được kiểm thử và điều kiện kiểm thử

### 1.1. Nguyên mẫu

Thiết bị đeo cổ tay hoàn chỉnh, chạy độc lập bằng pin, xử lý toàn bộ trên chip:

| Thành phần | Cấu hình |
| :--- | :--- |
| Vi điều khiển | Seeed XIAO ESP32-S3, chạy FreeRTOS đa tác vụ |
| Cảm biến chuyển động | MPU6050 — gia tốc kế 3 trục, lấy mẫu 25 Hz |
| Cảm biến quang học | MAX30102 mặt lưng cổ tay, chế độ phản xạ, LED hồng ngoại 940nm |
| Cảm biến đối chứng | MAX30102 kẹp đầu ngón tay (chỉ dùng khi kiểm thử, không thuộc sản phẩm) |
| Lưu trữ | Bộ nhớ flash trên chip, ghi liên tục suốt phiên đo |
| Mô hình AI trên thiết bị | Decision Tree xuất sang mã C, chạy trực tiếp trên chip |

*Bảng 1: Cấu hình nguyên mẫu đưa vào kiểm thử.*

### 1.2. Điều kiện kiểm thử thực tế

Kiểm thử **không** thực hiện trong điều kiện phòng thí nghiệm lý tưởng. Thiết bị được đeo
lên cổ tay người thật, chạy bằng pin, không nối dây với máy tính trong suốt phiên đo.

| Yếu tố | Điều kiện thực tế áp dụng |
| :--- | :--- |
| Số người tham gia | **18 người** cho phân hệ nhận diện hoạt động; 5 người có đủ hai kênh quang học |
| Thời lượng mỗi phiên | ~7,5 phút liên tục, không dừng giữa chừng |
| Hoạt động | 5 trạng thái vận động thật: nằm, ngồi, đứng, đi bộ, chạy |
| Nguồn điện | Pin LiPo, không cắm dây |
| Truyền dữ liệu | Ghi vào bộ nhớ trong; Bluetooth chỉ để theo dõi |
| Nhiễu | Không kiểm soát cử động tự phát của người tham gia |

*Bảng 2: Điều kiện kiểm thử.*

Một ràng buộc quan trọng chi phối toàn bộ thiết kế kiểm thử: **mỗi người tham gia chỉ đo một
lần duy nhất**. Không có phiên đo lại. Điều này buộc quy trình kiểm thử phải phát hiện lỗi
**ngay trong lúc đo**, không phải sau khi phân tích.

---

## 2. Quy trình kiểm thử

Nguyên mẫu được kiểm thử ở **ba tầng độc lập**, mỗi tầng bắt được một loại lỗi mà tầng khác
không thấy.

### 2.1. Tầng 1 — Kiểm thử giao thức thu dữ liệu

![Hình 1: Cấu trúc một phiên đo. 15 giây chuẩn bị, 5 hoạt động mỗi hoạt động 90 giây, giữa các hoạt động có khoảng đệm bị loại khỏi phân tích.](weekly_reports/figures/week06_protocol_timeline.png)

Mỗi phiên đo theo một trình tự cố định để nhãn dữ liệu luôn xác định được từ đồng hồ giao
thức, không phụ thuộc vào phán đoán của con người hay của mô hình.

**Kiểm tra ngay trong lúc đo:** hai chỉ báo hiển thị trực tiếp cho người vận hành — cảm biến
có đang áp đúng vào da không, và còn bao nhiêu giây nữa hết động tác hiện tại.

### 2.2. Tầng 2 — Kiểm thử mô hình trên dữ liệu, độc lập người dùng

![Hình 2: Mỗi vòng đánh giá, một người bị giữ riêng ra làm bài kiểm tra; mô hình chỉ được học từ 17 người còn lại. Lặp lại đủ 18 vòng.](weekly_reports/figures/week09_logocv.png)

Mô hình được đánh giá bằng **LOGO-CV (Leave-One-Group-Out Cross-Validation)** — giữ riêng
trọn vẹn từng người ra làm tập kiểm thử, mô hình chỉ học từ 17 người còn lại, lặp lại đủ 18
vòng.

**Vì sao chọn cách này:** nếu chia dữ liệu ngẫu nhiên theo dòng, các cửa sổ thời gian liền kề
của cùng một người sẽ nằm ở cả tập huấn luyện lẫn tập kiểm thử. Mô hình chỉ cần nhớ đặc điểm
riêng của người đó là đạt điểm cao — con số rất đẹp nhưng vô nghĩa, vì trong thực tế thiết bị
luôn gặp người dùng mới. LOGO-CV cho con số **thật sự khi gặp người lạ**.

### 2.3. Tầng 3 — Kiểm thử trên phần cứng thật

![Hình 3: Chuỗi ba bước đưa mô hình từ máy tính lên chip. Bước nối mô hình mới vào chương trình đang chạy từng bị bỏ sót, chỉ lộ ra khi nạp thử lên thiết bị.](weekly_reports/figures/week11_train_to_device.png)

Mô hình huấn luyện trên máy tính được xuất sang mã C, nạp lên chip, rồi **đeo lên cổ tay và
chạy trực tiếp**. Đây là tầng kiểm thử duy nhất bắt được các lỗi phát sinh khi chuyển từ máy
tính sang phần cứng.

### 2.4. Các thước đo sử dụng

| Thước đo | Dùng cho | Vì sao chọn |
| :--- | :--- | :--- |
| Accuracy theo LOGO-CV | Nhận diện hoạt động | Đo hiệu năng trên người dùng mới, không phải người đã học |
| Recall từng lớp | Nhận diện hoạt động | Một con số trung bình che mất chỗ hỏng cụ thể |
| Majority-class baseline | Nhận diện hoạt động | Không có mốc sàn thì một con số accuracy không mang ý nghĩa |
| MAE (bpm) | Đo nhịp tim | Thước đo bắt buộc theo chuẩn ANSI/AAMI EC13 |
| Signal Yield Rate | Đo nhịp tim | Trước khi bàn sai số, phải biết bao nhiêu phần trăm thời gian đọc được tín hiệu |
| Phép thử sinh lý học | Kiểm chứng dữ liệu đối chứng | Nhịp tim khi chạy bắt buộc phải cao hơn khi nằm |

*Bảng 3: Sáu thước đo và lý do lựa chọn.*

---

## 3. Kết quả kiểm thử chính

### 3.1. Phân hệ nhận diện hoạt động

| Cấu hình | Accuracy (LOGO-CV, 18 người) | Ghi chú |
| :--- | ---: | :--- |
| 5 lớp (nằm/ngồi/đứng/đi/chạy) | 54,8% | Cấu hình theo cam kết ban đầu |
| **3 lớp (nghỉ/đi/chạy)** | **85,3%** | Sau khi định nghĩa lại bài toán, xem mục 6.1 |

Recall từng lớp ở cấu hình 5 lớp cho thấy sai số **không phân bố đều**:

| Hoạt động | Recall | Đánh giá |
| :--- | ---: | :--- |
| Nằm | 28,4% | Gần mức đoán ngẫu nhiên (20%) |
| Ngồi | 46,9% | Nhầm nặng với đứng |
| Đứng | 55,1% | Nhầm nặng với ngồi |
| Đi bộ | 64,6% | Tách biệt rõ khỏi nhóm tĩnh |
| Chạy | 78,2% | Tách biệt hoàn toàn |

*Bảng 4: Recall từng lớp — toàn bộ sai số tập trung vào ba tư thế tĩnh.*

**Kết quả chạy trực tiếp trên thiết bị** (đeo lên cổ tay, phân loại thời gian thực):

| Hoạt động | Nhận đúng khi chạy trực tiếp |
| :--- | ---: |
| Chạy | **99%** |
| Đứng | **76%** |
| Nằm / Ngồi | Vẫn nhầm sang đứng |

*Bảng 5: Kết quả chạy trực tiếp trên phần cứng.*

Điểm quan trọng: **hướng nhầm lẫn khi chạy thật khớp chính xác với dự đoán từ giai đoạn huấn
luyện.** Điều này xác nhận toàn bộ chuỗi *huấn luyện → xuất mã → nạp thiết bị* hoạt động
đúng, không phát sinh sai lệch mới khi tích hợp.

### 3.2. Phân hệ đo nhịp tim

![Hình 4: Tỉ lệ thời gian tín hiệu thực sự chứa nhịp đập đọc được. Chuyển từ đầu ngón tay sang cổ tay làm mất gần ba phần tư lượng thông tin.](figures/hr_coverage_by_signal.png)

| Tín hiệu | Tỉ lệ cửa sổ đọc được nhịp tim hợp lệ |
| :--- | ---: |
| Đầu ngón tay (kênh đối chứng) | 35,0% |
| **Cổ tay, không lọc** | **9,6%** |
| Cổ tay + NLMS | 8,0% |
| Cổ tay + RLS | 5,5% |
| Cổ tay + Wiener | 12,7% |

*Bảng 6: Signal Yield Rate — chỉ số quan trọng nhất của phân hệ này.*

Kết luận không phụ thuộc vào ngưỡng chấp nhận đã chọn. Quét toàn dải từ lỏng đến khắt khe:
càng đòi hỏi tín hiệu phải mang đúng đặc tính nhịp điệu sinh lý, tỉ lệ đọc được ở cổ tay càng
suy giảm — ở mức khắt khe nhất chỉ còn **1,6%** so với 19,6% của đầu ngón tay, tức chênh
**12,2 lần**.

---

## 4. Đối chiếu với yêu cầu dự án

| Yêu cầu trong đề cương | Kết quả kiểm thử | Trạng thái |
| :--- | :--- | :--- |
| Dataset ≥ 10 người tham gia | 18 người | **Vượt** |
| Thí nghiệm đối chứng cổ tay / đầu ngón tay, ≥ 5 người | Đúng 5 người, đủ hai kênh | **Đạt** |
| Nhận diện hoạt động ≥ 85% trên người chưa từng gặp | 3 lớp đạt 85,3%; 5 lớp đạt 54,8% | **Đạt có điều kiện** |
| Phân loại 5 lớp — hạng mục bắt buộc | Thu về 3 lớp | Đổi hướng, có căn cứ đo được |
| Đo nhịp tim dùng được trên thực tế | Signal Yield 9,6% | **Không đạt** |
| Mô hình chạy trực tiếp trên vi điều khiển | Có, đã kiểm chứng trên tay người | **Đạt** |

*Bảng 7: Đối chiếu kết quả kiểm thử với yêu cầu dự án.*

**Về dòng "đạt có điều kiện":** ngưỡng 85% được đáp ứng, nhưng trên bài toán đã thu hẹp từ 5
lớp xuống 3 lớp. Báo cáo này không trình bày điều đó như một thành công trọn vẹn — lý do thu
hẹp và căn cứ của nó nằm ở mục 5.1 và 6.1.

---

## 5. Các vấn đề phát hiện được qua kiểm thử

Bốn vấn đề dưới đây đều **chỉ lộ ra nhờ kiểm thử**, và ba trong bốn vấn đề đã vượt qua mọi
kiểm tra tự động trước đó.

### 5.1. Vấn đề 1 — Ba tư thế tĩnh không thể phân biệt được (giới hạn cấu trúc)

**Phát hiện bằng:** phân rã recall theo từng lớp (Bảng 4), sau đó truy nguyên bằng lập luận
toán học.

![Hình 5: Gia tốc thô của cả 5 hoạt động trên cùng một thang đo. Ba tư thế tĩnh là ba đường gần như phẳng, không phân biệt được bằng mắt lẫn bằng số.](figures/waveform_by_activity.png)

Cả bốn đặc trưng đưa vào mô hình đều tính từ **độ lớn** gia tốc, tức `√(ax² + ay² + az²)` —
chính là **độ dài** của vector gia tốc. Khi cổ tay xoay, vector đổi **hướng** nhưng **không
đổi độ dài**. Mà nằm, ngồi, đứng khác nhau đúng ở hướng cổ tay.

Bằng chứng số trực tiếp: giá trị `mean_mag` trung vị của nằm / ngồi / đứng / đi bộ lần lượt là
**2000 · 1828 · 1896 · 1937** — bốn tư thế cơ thể khác hẳn nhau nhưng độ lớn gia tốc gần như y
hệt, tất cả đều xấp xỉ 1g, tức chỉ đang đo **trọng lực**.

→ **Kết luận:** đây là **giới hạn cấu trúc của bộ đặc trưng**, không phải lỗi chọn tham số.
Thông tin cần thiết đã bị xoá ngay ở bước tính đặc trưng, trước khi mô hình nhìn thấy dữ liệu.
Không có cách tinh chỉnh mô hình nào khôi phục được.

### 5.2. Vấn đề 2 — Sáu phiên đo không có người đeo thiết bị

**Phát hiện bằng:** vẽ dạng sóng thô ra và đối chiếu với kỳ vọng vật lý.

![Hình 6: Quy tắc tự động quét toàn bộ 21 phiên đo. Sáu phiên bị loại là những lần thử thiết bị — chúng đã vượt qua mọi kiểm tra tự động trước đó.](weekly_reports/figures/week08_quality_gate.png)

Sáu phiên đo có đủ số nhãn, đủ số dòng dữ liệu, log không báo lỗi — nhưng thiết bị nằm yên
trên bàn, không có người đeo. Chúng chỉ lộ ra khi có người vẽ dạng sóng lên và hỏi: *tại sao
đoạn "đang chạy" lại phẳng như đoạn "đang nằm"?*

→ **Mức nghiêm trọng:** nếu sáu phiên này lọt vào tập huấn luyện, mô hình sẽ được dạy rằng
chạy bộ trông giống nằm yên. Mọi con số về sau đều sai, và không có cách nào lần ra nguồn gốc.

### 5.3. Vấn đề 3 — Thước đo đối chứng sai gấp đôi

**Phát hiện bằng:** phép thử sinh lý học — *nhịp tim khi chạy có cao hơn khi nằm không?*

![Hình 7: Nhịp tim đo từ kênh đối chứng đầu ngón tay theo từng hoạt động. Kênh này trượt phép thử sinh lý ở 3 trên 5 người.](figures/gt_sanity_by_activity.png)

Kênh đối chứng đầu ngón tay — vốn được giả định là chuẩn sạch — **trượt phép thử ở 3 trên 5
người**. Trường hợp nặng nhất ghi nhận **đứng yên 127,7 bpm nhưng chạy chỉ 89,7 bpm**.

Truy nguyên bằng cách vẽ dạng sóng thô và đếm đỉnh thủ công: dạng sóng **rất sạch**, đếm được
30 đỉnh trong 12 giây tức 155,6 bpm, trong khi thuật toán báo **77,0 bpm** — đúng một nửa.

Đã loại trừ cách giải thích cạnh tranh: nếu mỗi nhịp bị đếm thành hai đỉnh, khoảng cách giữa
các đỉnh phải so le dài-ngắn. Đo được tỉ lệ khoảng lẻ/chẵn = **1,03** (đều tăm tắp), còn tỉ lệ
biên độ lẻ/chẵn = **2,22**. Vậy thứ so le là **biên độ**, không phải khoảng cách.

→ **Cơ chế:** biên độ nhịp cao–thấp xen kẽ khiến dạng sóng lặp lại sau mỗi *hai* nhịp, tạo
thành phần phổ mạnh ở đúng nửa nhịp thật. Thuật toán bám vào đó.

→ **Vì sao sống sót lâu:** lỗi phát sinh ở tầng đo, nhưng bộ chặn giá trị bất thường lại nằm ở
tầng làm mượt. Khi tầng đo liên tục trả về dãy [77, 77, 77, …] cực kỳ nhất quán, tầng làm mượt
tin tưởng hoàn toàn; khi tầng đo thỉnh thoảng bắt đúng 156, tầng làm mượt **gạt đi**. Hệ thống
đã chủ động bảo vệ con số sai.

### 5.4. Vấn đề 4 — Sai bước sóng quang học cho vị trí đo

**Phát hiện bằng:** kết quả Signal Yield sau khi đã sửa thước đo (Bảng 6).

| Bước sóng | Hemoglobin hấp thụ | Phù hợp với |
| :--- | :--- | :--- |
| ~525 nm (xanh lá) | **Rất mạnh** | Đo phản xạ tại cổ tay — đồng hồ thương mại dùng |
| 660 nm (đỏ) | Yếu | Đo SpO2, đo xuyên thấu tại đầu ngón tay |
| 940 nm (hồng ngoại) | Yếu | Đo SpO2, đo xuyên thấu tại đầu ngón tay |

*Bảng 8: Đặc tính hấp thụ quang học của từng bước sóng.*

MAX30102 chỉ phát được đỏ và hồng ngoại — hai bước sóng máu hầu như **không hấp thụ**. Ở cổ
tay, chúng xuyên sâu nhưng phần lớn ánh sáng dội về đến từ mô sâu, gân và xương, nên nhịp đập
chỉ là gợn sóng rất nhỏ trên nền lớn.

→ **Kết luận:** đây là *"dùng đúng cảm biến cho sai vị trí giải phẫu"*. Vị trí cổ tay không
sai — đồng hồ thương mại cũng đeo ở đó. Sai ở **bước sóng**.

---

## 6. Các cải tiến đã thực hiện dựa trên kết quả kiểm thử

Mỗi cải tiến dưới đây đều được kích hoạt bởi một kết quả kiểm thử cụ thể, không phải bởi phán
đoán trước.

| # | Cải tiến | Kích hoạt bởi | Kết quả sau cải tiến |
| :--- | :--- | :--- | :--- |
| 1 | Thêm 15 giây chuẩn bị trước động tác đầu; âm thanh nhắc chuyển từ máy tính | Nhãn sai ngay giây đầu mỗi phiên | Nhãn khớp thực tế từ đầu phiên |
| 2 | Kiểm tra cảm biến áp da liên tục thay vì một lần lúc khởi động | Cảm biến lệch giữa phiên mà không ai biết | Phát hiện được ngay trong lúc đo |
| 3 | Ngưỡng nhận diện nhịp tự điều chỉnh theo từng người | Nhịp tim đứng yên hàng chục giây | Đo liên tục, không còn khoảng chết |
| 4 | Quy tắc tự động loại phiên đo không có người đeo | Vấn đề 2 (mục 5.2) | 6 / 21 phiên bị loại đúng |
| 5 | Gỡ đoạn logic ép mặc định "nằm" khi thiết bị đứng yên | Kiểm thử trên phần cứng thật | Mô hình mới hoạt động đúng chức năng chính |
| 6 | **Định nghĩa lại bài toán từ 5 lớp về 3 lớp** | Vấn đề 1 (mục 5.1) | **54,8% → 85,3%** |
| 7 | **Thay thế bộ ước lượng nhịp tim (Estimator v2)** | Vấn đề 3 (mục 5.3) | Qua kiểm tra sinh lý: **2/5 → 4/5 người** |

*Bảng 9: Bảy cải tiến, mỗi cải tiến truy được về kết quả kiểm thử đã kích hoạt nó.*

### 6.1. Chi tiết cải tiến số 6 — Định nghĩa lại bài toán

![Hình 8: Ba tư thế tĩnh được gộp thành một nhóm. Đây không phải chọn cách chia cho ra số đẹp hơn, mà là định nghĩa lại bài toán cho khớp với thứ cảm biến đo được.](weekly_reports/figures/week12_regroup.png)

Giữ nguyên tuyệt đối mô hình, bốn đặc trưng, bộ dữ liệu và giao thức đánh giá — chỉ gộp ba tư
thế tĩnh thành một nhóm.

**Đây có phải chọn cách chia cho ra số đẹp không?** Không, vì hai lý do:

1. **Ranh giới gộp được suy ra trước khi nhìn kết quả**, từ nguyên nhân gốc ở mục 5.1.
2. **Việc gộp loại bỏ đúng phần bộ đặc trưng không quan sát được**, giữ nguyên phần nó quan
   sát rất tốt.

**Đánh giá công bằng — đối chiếu với mốc sàn:**

| Bài toán | Mốc sàn (đoán lớp đông nhất) | Accuracy đo được | Biên vượt mốc sàn |
| :--- | ---: | ---: | ---: |
| 5 lớp | 0,201 | 0,548 | **+0,347** |
| 3 lớp | 0,599 | 0,853 | **+0,254** |

*Bảng 10: So sánh công bằng với mốc sàn của từng bài toán.*

→ **Ghi nhận trung thực:** so thẳng 54,8% với 85,3% là **phóng đại mức cải thiện**. Bài toán 3
lớp dễ hơn về mặt cấu trúc vì lớp "nghỉ" chiếm 60% dữ liệu. Thước đo công bằng là biên vượt
mốc sàn riêng — và theo thước đo đó, phần mô hình **thực sự học được** ở bài toán 3 lớp
(+0,254) lại **nhỏ hơn** ở bài toán 5 lớp (+0,347).

### 6.2. Chi tiết cải tiến số 7 — Thay thế bộ ước lượng nhịp tim

Bộ ước lượng mới thay đổi ba điểm: đo **trung vị khoảng cách giữa các nhịp** trong miền thời
gian thay vì bám đỉnh phổ; **trả về "không đọc được"** khi nhịp quá không đều thay vì đoán
bừa; và **bỏ hoàn toàn ràng buộc liên tục** giữa các cửa sổ.

| Trường hợp kiểm chứng | Bộ cũ | Bộ mới | Đếm thủ công |
| :--- | ---: | ---: | ---: |
| Đối tượng A lúc chạy | 77,0 | **156,9** | 155,6 |
| Đối tượng B lúc chạy | 155,8 | **118,9** | 111,3 |
| Số người qua kiểm tra sinh lý | 2/5 | **4/5** | — |

*Bảng 11: Kiểm chứng bộ ước lượng mới bằng đếm đỉnh thủ công.*

Bộ mới sửa sai số theo **cả hai chiều** — một trường hợp bị đọc thiếu một nửa, trường hợp kia
bị đọc thừa. Điều này xác nhận nó hoạt động dựa trên cơ chế vật lý thật, không phải một phép
hiệu chỉnh một chiều tình cờ trúng.

---

## 7. Kết quả kiểm thử đã thay đổi hướng đi của dự án như thế nào

Đề cương ban đầu đặt câu hỏi: *thuật toán lọc nhiễu nào — LMS, RLS hay Wiener — khử nhiễu
chuyển động khỏi PPG cổ tay tốt nhất?*

Kết quả kiểm thử ở mục 3.2 cho thấy **tiền đề của câu hỏi này không thoả mãn**. Trong khoảng
90% thời gian, tín hiệu cổ tay ở cấu hình phần cứng hiện tại không chứa nhịp đập nào để mà
khử nhiễu. Bộ lọc *tách* tín hiệu ra khỏi nhiễu — nó không *tạo ra* tín hiệu.

Đây là lý do dự án chuyển trọng tâm từ **tối ưu thuật toán** sang **truy nguyên giới hạn phần
cứng**. Việc chuyển hướng này không phải một lựa chọn về sở thích, mà là **hệ quả trực tiếp
của kết quả kiểm thử**:

| Nếu tiếp tục theo hướng cũ | Kết quả kiểm thử cho thấy |
| :--- | :--- |
| Tinh chỉnh tham số ba bộ lọc | Cả ba đều làm tệ đi, vì trừ luôn cả phần tín hiệu ít ỏi còn lại |
| Thử thêm bộ lọc thứ tư | Không thay đổi được việc đầu vào không chứa nhịp đập |
| Tăng số người tham gia | Không thay đổi được đặc tính quang học của bước sóng |

*Bảng 12: Vì sao tiếp tục hướng cũ không giải quyết được vấn đề.*

Kết quả cuối cùng của phân hệ đo nhịp tim vì vậy là một **kết quả âm tính đã được kiểm chứng
chặt chẽ**: bộ lọc phần mềm không thể bù đắp cho việc chọn sai bước sóng quang học ở tầng thu
tín hiệu. Giả thuyết ban đầu — *phần cứng giá rẻ cộng thuật toán tốt có thể thay thế phần cứng
chuyên dụng* — đã bị bác bỏ bằng thực nghiệm, chứ không phải bị bỏ dở.

---

## 8. Bài học rút ra từ quá trình kiểm thử

Ba trong bốn vấn đề ở mục 5 đều **vượt qua mọi kiểm tra tự động** và chỉ bị phát hiện bằng
kiểm chứng vật lý:

| Vấn đề | Chỉ số nói gì | Thực tế | Phát hiện bằng |
| :--- | :--- | :--- | :--- |
| 6 phiên đo giả | "Đủ nhãn, đủ dòng, không lỗi" | Không ai đeo thiết bị | Vẽ dạng sóng ra nhìn |
| Ba tư thế tĩnh | "Accuracy 54,8% — mô hình tầm thường" | Bộ đặc trưng mù hoàn toàn với 3 lớp | Lập luận toán học ba dòng |
| Thước đo sai gấp đôi | "MAE ~27 bpm — bộ lọc vô dụng" | Thước đo sai một nửa | Hỏi "chạy có cao hơn nằm không?" |

*Bảng 13: Ba lỗi vượt qua mọi kiểm tra tự động.*

Cả ba lỗi đều **nhất quán về mặt số học** — chuỗi [77, 77, 77, …] rất đều; ma trận nhầm lẫn
rất ổn định qua 18 vòng đánh giá. Chính sự nhất quán đó giúp chúng vượt qua mọi kiểm tra tự
động: các chỉ số kiểm tra dữ liệu **có ăn khớp với nhau không**, chứ không kiểm tra dữ liệu
**có đúng với thực tế vật lý không**.

**Nguyên tắc rút ra:** mỗi tín hiệu tham chiếu cần ít nhất một phép thử đối chiếu với quy luật
vật lý hoặc sinh lý đã biết. Ba phép thử phát hiện ra ba lỗi trên đều tốn **dưới 15 phút**, và
đều nằm ngoài mọi quy trình đánh giá tự động.

---

## 9. Danh mục bằng chứng kèm theo

| Loại bằng chứng | Nội dung | Vị trí |
| :--- | :--- | :--- |
| Dữ liệu đo | 18 người tham gia, 20.258 cửa sổ dữ liệu (16.880 sau khi lọc đoạn chuyển tiếp) | `data/processed/master_dataset.csv` |
| Dữ liệu thô | Tín hiệu thô 6 kênh của 5 người có đủ hai kênh quang học | `experiments/wrist/valid_sessions/` |
| Nhật ký kiểm thử | Trạng thái từng phiên đo, gồm cả các phiên bị loại và lý do | `experiments/wrist/session_manifest.csv` |
| Mã kiểm thử | 12 script, mọi con số tái tạo được bằng một lệnh | Xem `paper/EVIDENCE_GUIDE.md` |
| Biểu đồ đo đạc | 11 biểu đồ sinh trực tiếp từ dữ liệu, không vẽ tay | `paper/figures/` |
| Mã nguồn firmware | Phần tính đặc trưng chạy trên thiết bị | `firmware_ble/main.cpp`, dòng 738–750 |

*Bảng 14: Danh mục bằng chứng.*

**Tính tái lập:** mọi script đều cố định `random_state = 0`, không có yếu tố ngẫu nhiên. Chạy
lại bao nhiêu lần cũng cho đúng một kết quả. Quy trình chạy lại từng con số được ghi trong
`paper/EVIDENCE_GUIDE.md`.

**Bằng chứng chưa có:** báo cáo này chưa kèm ảnh chụp và video của buổi kiểm thử trên phần
cứng. Kết quả chạy trực tiếp ở Bảng 5 được ghi lại dưới dạng nhật ký dữ liệu, không phải bản
ghi hình.

---

## 10. Kết luận

Nguyên mẫu đã được kiểm thử trong điều kiện thực tế trên 18 người tham gia, ở ba tầng độc lập:
giao thức thu dữ liệu, đánh giá mô hình độc lập người dùng, và chạy trực tiếp trên phần cứng.

**Đạt yêu cầu:** phân hệ nhận diện hoạt động đạt 85,3% trên người dùng chưa từng gặp, chạy
được trực tiếp trên vi điều khiển, và kết quả trên phần cứng thật khớp với kết quả trên máy
tính.

**Không đạt yêu cầu:** phân hệ đo nhịp tim, với nguyên nhân đã truy được đến tầng phần cứng —
sai bước sóng quang học cho vị trí đo phản xạ ở cổ tay.

**Giá trị của quá trình kiểm thử:** bốn vấn đề được phát hiện, trong đó ba vấn đề đã vượt qua
mọi kiểm tra tự động và chỉ lộ ra nhờ kiểm chứng vật lý. Bảy cải tiến được thực hiện, mỗi cải
tiến truy được về kết quả kiểm thử đã kích hoạt nó. Quan trọng nhất, kiểm thử đã phát hiện
rằng một kết quả tưởng đã hoàn tất thực ra được đo bằng một thước đo hỏng — và kịp sửa trước
khi nó đi vào kết luận cuối cùng.
