# Đối chiếu Proposal và Thực tế — Wearable Activity & Health Monitor

> **Ghi chú về tác giả:** bảng đối chiếu và phần justify dưới đây do Claude soạn từ
> việc rà repo, chạy lại toàn bộ script, và đọc `archived/project_description.md`.
> Mọi con số đều verify được bằng lệnh ghi trong `paper/EVIDENCE_GUIDE.md`. Những
> mục Claude **chưa** kiểm chứng được đánh dấu rõ ở Phần 5 — Giang cần tự xác nhận
> trước khi nộp.
>
> **Ngày rà soát:** 2026-08-15 · **Proposal gốc:** `archived/project_description.md`

---

## 1. Tài liệu này để làm gì

Proposal viết ở tuần 0, khi chưa ai chạm vào dữ liệu thật. Sau 13 tuần, một số điều
trong đó đã đạt, một số phải đổi hướng, và một số hoá ra dựa trên giả định sai.

Tài liệu này liệt kê **từng chỗ lệch một**, và với mỗi chỗ trả lời ba câu:
lệch cái gì · vì sao · bằng chứng nào cho phép kết luận như vậy.

Nguyên tắc: không có chỗ lệch nào được biện minh bằng "hết thời gian". Hoặc là có
lý do kỹ thuật đo được, hoặc là ghi thẳng đó là thiếu sót.

---

## 2. Bảng tổng hợp

| # | Proposal cam kết | Thực tế | Trạng thái |
| :-- | :--- | :--- | :--- |
| 1 | Dataset ≥ 10 participant | 18 participant | **Vượt** |
| 2 | M6: fingertip vs wrist, ≥ 5 participant | Đúng 5 participant, session ~7.5 phút mỗi người | **Đạt** |
| 3 | HAR accuracy ≥ 85% trên người chưa từng gặp *(pass/fail)* | 3-class 85.3% · 5-class 54.8% | **Đạt có điều kiện** |
| 4 | Phân loại 5 hoạt động — *core, must deliver* | Thu về 3 nhóm (stationary/walking/running) | Đổi hướng, có justify |
| 5 | Input: MPU6050 cấp accel **+ gyroscope 3 trục** | Gyroscope không được đọc dòng nào | Thiếu sót, hậu quả đã đo được |
| 6 | Feature miền tần số (dominant freq, spectral entropy) cho HAR | Chỉ dùng 4 feature miền thời gian | Đổi hướng, có justify |
| 7 | M3: TFLite Micro int8 model | Decision Tree xuất ra C header | Đổi hướng, có justify |
| 8 | M4: LMS filter **chạy trong firmware** | Chỉ chạy offline bằng Python | Đổi hướng, có justify |
| 9 | RQ: LMS/RLS/Wiener — cái nào tốt nhất? | Tiền đề câu hỏi sai; xem §4 | **Trả lời được, theo hướng khác** |
| 10 | Heart rate (BPM) — *core, must deliver* | Không đạt độ chính xác dùng được | **Không đạt** |
| 11 | PPG: MAX30102, 660nm + 940nm, đeo mặt lưng cổ tay | Sai bước sóng cho vị trí này | **Sai lầm thiết kế phần cứng** |
| 12 | Fingertip = *"clean ground truth, minimal motion artifact"* | Cảm biến tốt, nhưng hàm ước lượng BPM hỏng | **Giả định chưa kiểm chứng** |
| 13 | Web BLE dashboard thời gian thực | Thư mục `dashboard/` rỗng | **Không đạt** |
| 14 | SpO2 / fall detection / sleep stage (optional) | Ngoài scope | Đúng như proposal đã rào |

---

## 3. Những chỗ đổi hướng — và lý do

### 3.1 Từ 5 lớp xuống 3 lớp *(dòng 3, 4)*

**Đổi gì:** gộp lying/sitting/standing thành một lớp `stationary`.

**Vì sao:** cả 4 feature đều tính từ **magnitude** của vector gia tốc, mà magnitude là
đại lượng **bất biến với phép xoay** — nó chỉ phản ánh cường độ chuyển động, không mang
thông tin về hướng. Ba tư thế tĩnh khác nhau **duy nhất** ở hướng cổ tay so với trọng
lực. Nói cách khác, thông tin cần thiết đã bị xoá ngay ở bước tính đặc trưng, trước khi
model nhìn thấy dữ liệu. Không có lựa chọn hyperparameter nào khôi phục được nó.

**Bằng chứng:** median `std_mag` của ba tư thế tĩnh là 17.6 / 25.3 / 31.9 trong khi độ
trải của mỗi lớp là 65–95 — ba phân phối chồng lên nhau gần như hoàn toàn. Ba lần thử
đặc trưng per-axis đều không generalize (`CHANGELOG.md`, 2026-07-22 → 07-28).

**Về dòng 3, phải nói rõ để không bị hiểu nhầm:** chuẩn "≥ 85% trên người chưa từng gặp"
được đáp ứng ở mức 85.3%, nhưng **trên bài toán đã thu hẹp**. Đây không phải đạt chuẩn
như proposal hình dung. Bài toán 5 lớp đúng như cam kết ban đầu chỉ đạt 54.8%.

### 3.2 Bỏ feature miền tần số *(dòng 6)*

**Vì sao:** với cửa sổ 2.4 giây ở 25 Hz (60 mẫu), độ phân giải tần số quá thô để
spectral entropy nói lên điều gì hữu ích cho việc phân biệt tư thế tĩnh — vốn là chỗ
bài toán thực sự khó. Bốn feature miền thời gian đã đủ để tách nhóm tĩnh khỏi nhóm động
(tỉ số 15.7×), và phần còn thiếu là thông tin **hướng**, thứ mà không feature tần số nào
lấy lại được.

**Ghi chú:** phân tích phổ **có** được dùng, nhưng ở subsystem B (ước lượng nhịp tim),
không phải ở HAR.

### 3.3 Decision Tree thay cho TFLite Micro *(dòng 7)*

**Vì sao:** 4 feature và 18 participant là quy mô mà một mạng nơ-ron lượng tử hoá không
mang lại lợi ích gì ngoài rủi ro overfit — chính LOGO-CV đã cho thấy độ dao động giữa
người với người còn lớn hơn nhiều so với khoảng cách giữa các lựa chọn model. Decision
Tree chạy trong vài micro giây, xuất thẳng ra C header, và **đọc được từng luật** — thuộc
tính có giá trị hơn hẳn khi cần giải thích vì sao model sai.

**Cái phải thừa nhận:** đây cũng đồng nghĩa với việc mục tiêu học TFLite Micro trong
proposal không đạt.

### 3.4 LMS chạy offline thay vì trong firmware *(dòng 8)*

**Vì sao:** thứ tự hợp lý là chứng minh bộ lọc có tác dụng **trước**, rồi mới nạp lên
thiết bị. Kết quả offline cho thấy không bộ lọc nào cải thiện được nhịp tim (§4), nên
việc nạp lên firmware sẽ là tối ưu hoá một thứ vô dụng.

**Đây là chỗ đổi hướng đúng.** Nếu làm theo đúng proposal — cài LMS vào firmware ở tuần 7
rồi mới đo — thì đã tốn công vào một hướng mà dữ liệu chứng minh là không có cửa.

---

## 4. Câu hỏi nghiên cứu: trả lời được, nhưng không theo cách đã hình dung *(dòng 9, 10, 11, 12)*

Proposal hỏi: *"trên phần cứng ESP32, thuật toán nào — LMS, RLS hay Wiener — khử nhiễu
chuyển động khỏi PPG cổ tay tốt nhất, và có đạt độ chính xác nhịp tim dùng được không?"*

Quá trình trả lời đi qua ba tầng, mỗi tầng lật lại tầng trước.

**Tầng 1 — so sánh ban đầu.** Không bộ lọc nào thắng việc không lọc gì: MAE gộp lần lượt
26.95 (baseline) / 26.96 (NLMS) / 29.83 (RLS) / 29.96 (Wiener) bpm.

**Tầng 2 — nghi ngờ chính thước đo.** Toàn bộ MAE ở trên đo so với nhịp tim suy từ đầu
ngón tay. Proposal gọi kênh đó là *"clean ground truth"* và **giả định đó chưa từng được
kiểm chứng**. Một phép thử sinh lý mất 10 phút — *"chạy thì nhịp tim có cao hơn nằm
không?"* — cho thấy tham chiếu trượt ở 3/5 participant. Nặng nhất: P02 ghi nhận đứng yên
127.7 bpm nhưng chạy chỉ 89.7 bpm.

**Nguyên nhân gốc, đã xác định chính xác:** với P17 lúc chạy, dạng sóng đầu ngón tay
**rất sạch** — 30 nhịp trong 12 giây, khoảng cách 0.386 s ± 0.017 s. Nhịp thật là
**156 bpm**; thuật toán báo **77 bpm**, đúng một nửa. Cơ chế: biên độ các nhịp so le
cao-thấp (tỉ lệ 2.2×) khiến dạng sóng lặp lại sau mỗi *hai* nhịp, sinh ra thành phần phổ
mạnh ở đúng nửa nhịp thật — lỗi **octave error** kinh điển của các bộ dò cao độ. Rồi
ràng buộc `MAX_JUMP_BPM = 25` khoá cứng sai số đó lại: mọi cửa sổ sau muốn sửa lên đều
bị gạt vì "nhảy quá xa".

Đã loại trừ cách giải thích cạnh tranh (mỗi nhịp có hai đỉnh do dicrotic notch): nếu vậy
khoảng cách giữa các đỉnh phải **so le** dài-ngắn, thực tế tỉ lệ lẻ/chẵn là **1.03**.

**Bài học kiến trúc:** `MAX_JUMP_BPM` thuộc **tracking layer** (đánh giá một dãy số theo
thời gian) nhưng đã được cho quyền phủ quyết **measurement layer** (đọc một con số từ
một cửa sổ sóng). Một bộ lọc làm mượt chỉ khử được *noise*, không khử được *bias* — nó
sẽ bám theo một sai số hệ thống một cách mượt mà và trông rất đáng tin. Đây là lý do bug
sống sót suốt nhiều tuần.

**Tầng 3 — sửa thước rồi đo lại.** Hàm ước lượng mới (`hr_estimator_v2.py`) đo trung vị
khoảng cách giữa các nhịp trong miền thời gian, **trả về "không đọc được"** khi nhịp quá
loạn thay vì đoán bừa, và bỏ hoàn toàn ràng buộc liên tục.

| Kiểm chứng | v1 | v2 | Đếm tay |
| :--- | ---: | ---: | ---: |
| P17 lúc chạy | 77.0 | **156.9** | 155.6 |
| P16 lúc chạy | 155.8 | **118.9** | 111.3 |
| Số người qua sanity check | 2/5 | **4/5** | — |

Chạy lại toàn bộ so sánh với thước mới cho ra **kết quả thật sự của subsystem B**:

| Tín hiệu | Tỉ lệ cửa sổ đọc được nhịp tim |
| :--- | ---: |
| Đầu ngón tay | 35.0% |
| **Cổ tay, không lọc** | **9.6%** |
| Cổ tay + NLMS | 8.0% |
| Cổ tay + RLS | 5.5% |
| Cổ tay + Wiener | 12.7% |

Và kết luận này không phụ thuộc vào ngưỡng đã chọn — càng đòi hỏi khắt khe thế nào là
một nhịp đập thật, tín hiệu cổ tay càng biến mất: ở ngưỡng chặt nhất còn **1.6%** so với
19.6% của đầu ngón tay, chênh **12×**.

**Câu trả lời cho câu hỏi nghiên cứu:** câu hỏi đặt sai tiền đề. Trong khoảng 90% thời
gian, PPG cổ tay ở cấu hình này **không chứa nhịp đập nào để mà khử nhiễu**. Bộ lọc
*tách* tín hiệu khỏi nhiễu, nó không *tạo ra* tín hiệu — nên việc xếp hạng LMS/RLS/Wiener
là vô nghĩa, không phải khó.

Quan sát phụ đáng ghi: NLMS và RLS làm **tệ đi** (MAE 47.3 và 58.3 so với 16.4). Hợp lý
về cơ chế — khi PPG gần như toàn nhiễu chuyển động, nghiệm tối ưu của một adaptive filter
là trừ đi gần hết mọi thứ, kể cả phần nhịp đập ít ỏi còn sót lại.

**Nguyên nhân vật lý *(dòng 11)*.** Proposal chốt MAX30102 với 660nm + 940nm, đeo mặt
lưng cổ tay. Hai bước sóng này **hầu như không bị hemoglobin hấp thụ** — chúng có mặt
trên MAX30102 để đo SpO2 và để đo **xuyên thấu** ở đầu ngón tay, nơi mật độ mạch máu rất
dày. Thiết bị đeo cổ tay thương mại dùng **LED xanh lá (~525nm)**, bước sóng bị máu hấp
thụ mạnh, nên một thay đổi nhỏ về thể tích máu mao mạch tạo ra thay đổi lớn về lượng ánh
sáng dội về. Đây là dùng **đúng cảm biến cho sai vị trí**. Vị trí đeo mặt lưng cổ tay thì
không sai — đồng hồ thương mại cũng đeo ở đó.

Hồ sơ dự án có một quyết định ghi rõ *"không cần module LED xanh — bộ lọc LMS sẽ xử lý độ
chính xác ở cổ tay"*. Kết quả ở trên cho thấy quyết định đó sai, và sai theo kiểu không
thuật toán nào bù được.

**Hệ quả cho dòng 10:** deliverable "Heart rate (BPM)" **không đạt**, và giờ đã biết
nguyên nhân nằm ở tầng thu tín hiệu chứ không phải tầng xử lý.

---

## 5. Những chuẩn Claude chưa kiểm chứng — Giang cần tự xác nhận

Bảng "Quantified Standards" của proposal có 5 chuẩn cho Giang. Lần rà này mới xác nhận
được một:

| Chuẩn | Trạng thái |
| :--- | :--- |
| HAR accuracy ≥ 85% trên người chưa gặp | Đã xác nhận — xem §3.1 |
| HAR inference latency ≤ 50ms | **Chưa kiểm chứng lại trong lần rà này** |
| BLE: 0 lần rớt ngoài ý muốn / 60 phút | **Chưa kiểm chứng** — và BLE từng bị tắt trong nhiều giai đoạn |
| Heap phẳng suốt 60 phút | **Chưa kiểm chứng lại** |
| Model RAM ≤ 100KB | **Chưa kiểm chứng lại** |

Bốn dòng cuối có số đo từ tuần 2 trong `CHANGELOG.md`, nhưng chúng đo trên
`firmware_baseline`, không phải firmware hiện tại. Nộp mà trích số cũ như thể là số hiện
tại thì đúng vào lỗi mà cả báo cáo này đang phê phán.

---

## 6. Những chỗ không đạt, không có biện minh

Hai mục dưới đây **không** có lý do kỹ thuật, chỉ là không làm kịp. Ghi ra đây thay vì
giấu vào phần "future work":

- **Web BLE dashboard** *(dòng 13)* — thư mục `dashboard/` rỗng. Đây là deliverable
  xuất hiện ở cả mục Output lẫn M10 của proposal.
- **Milestone M5, M7, M8** (PCB, tích hợp toàn hệ, chạy ổn định 60 phút) — thuộc phần
  việc của Duy và Tùng, nằm ngoài phạm vi rà soát này, chưa có bằng chứng trong repo.

---

## 7. Ba điều sẽ làm khác đi

**1. Kiểm chứng vật lý trước khi xây kiến trúc lên trên.** Cả hai sai lầm đắt nhất của
dự án đều thuộc cùng một dạng: tin vào một mô tả về thực tế thay vì đo thực tế. Bước sóng
sai lẽ ra phát hiện được bằng cách đeo cảm biến, ngồi im, nhìn dạng sóng thô — trước khi
thiết kế bất cứ thứ gì. Tham chiếu hỏng lẽ ra phát hiện được bằng câu hỏi *"chạy thì nhịp
tim có cao hơn nằm không?"*. Cả hai đều tốn dưới 15 phút. Cả hai đều không được làm.

Dự án đã từng mắc đúng lỗi này một lần nữa và tự bắt được: 6 phiên thu qua mọi kiểm tra ở
mức file nhưng thiết bị nằm im trên bàn không ai đeo, chỉ lộ ra khi vẽ dạng sóng thô
(`CHANGELOG.md`, 2026-07-22). Ba lần, cùng một dạng lỗi.

**2. Đọc mục "Applications" ở trang đầu datasheet trước khi chọn cảm biến.** Datasheet
MAX30102 ghi thẳng đối tượng sử dụng là đo ở **đầu ngón tay và dái tai**. Một trang giấy
đứng giữa dự án và mười tuần đi sai hướng.

**3. Không cho tầng làm mượt quyền phủ quyết tầng đo.** Ràng buộc liên tục đã giấu một
sai số 100% trong nhiều tuần vì nó khiến chuỗi kết quả trông nhất quán. Nếu tách bạch
hai tầng ngay từ đầu — measurement được phép trả về "không biết", tracking chỉ được làm
mượt — thì bug đã lộ ngay ở phiên thu đầu tiên có người chạy.

---

## 8. Đánh giá tổng thể

Trong 14 dòng đối chiếu: 2 vượt hoặc đạt, 1 đạt có điều kiện, 4 đổi hướng có căn cứ đo
được, 4 là sai lầm hoặc giả định chưa kiểm chứng đã được truy đến nguyên nhân gốc, 2
không đạt và không có biện minh, 1 đúng như đã rào trước.

Câu hỏi nghiên cứu ở mục 8 của proposal **đã được trả lời** — chỉ là câu trả lời hoá ra
là *"tiền đề của câu hỏi sai, và đây là bằng chứng vì sao"*. Với một dự án kỹ thuật, đó
là một kết quả hoàn chỉnh, không phải một chỗ bỏ trống.

**Tài liệu liên quan:** `SubsystemA_Wearable Device.md` (bộ phân loại hoạt động) ·
`paper/adaptive_filter_comparison_REPORT.md` (subsystem B) ·
`paper/EVIDENCE_GUIDE.md` (chạy lại từng con số).
