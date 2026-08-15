# Subsystem A — Wearable Device: Activity Classifier Finding

> **Ghi chú về tác giả (để tự kiểm tra trước khi nộp):** Toàn bộ *lập luận* trong báo
> cáo này là của Giang; Claude sửa wording, sắp xếp lại cấu trúc, và bổ sung phần
> Section 4 (phép so sánh với majority-class baseline) mà Giang chưa tự làm được.
> Ba chỗ lập luận gốc đã bị **sửa nội dung** (không chỉ wording) vì trái với số liệu
> thật — được đánh dấu bằng 🔧 tại chỗ. Đọc kỹ 3 chỗ đó trước khi nộp.
>
> **Nguồn số liệu:** mọi con số dưới đây lấy từ `train_activity_classifier.py` và
> `check_majority_baseline.py`, chạy lại trên `data/processed/master_dataset.csv`
> (18 participant; 20.258 dòng, còn 16.880 dòng sau khi loại các dòng chuyển tiếp
> tư thế) ngày 2026-08-13.

---

## 1. Finding (A)

**Kết quả chính:** với 4 đặc trưng dựa trên magnitude của gia tốc, bộ phân loại
5 lớp (lying / sitting / standing / walking / running) đạt **accuracy trung bình
0.548** theo giao thức **LOGO-CV trên N = 18 participant**.

| Lớp | Recall (5-class) |
| :--- | ---: |
| lying | 0.284 |
| sitting | 0.469 |
| standing | 0.551 |
| walking | 0.646 |
| running | 0.782 |
| **Mean accuracy** | **0.548** |

Mô hình: `DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, random_state=0)`.

### LOGO-CV là gì

LOGO-CV = Leave-One-Group-Out cross-validation, một cách chia tập train/test.

Khác với cách chia thông thường, ở đây mỗi participant sẽ lần lượt bị **cho ra
rìa** và biến thành test set, để kiểm tra xem model có "học vẹt" theo từng người
hay không. Cứ lặp lại như thế cho đến khi tất cả participant trong dataset đều
được làm test set đúng một lần — 18 người thì 18 vòng, accuracy báo cáo là trung
bình của 18 vòng đó.

Điểm khác cốt lõi: cross-validation thông thường chia dữ liệu theo **dòng ngẫu
nhiên**, còn LOGO-CV chia theo **nhãn định danh** (participant_id). Nếu chia
ngẫu nhiên theo dòng, các cửa sổ thời gian liền kề của *cùng một người* sẽ nằm
cả ở train lẫn test — model chỉ cần nhớ đặc điểm của người đó là đã đoán đúng,
và accuracy sẽ cao giả tạo. LOGO-CV chặn đúng lỗ hổng này, nên con số 0.548 là
ước lượng cho **người dùng mới chưa từng xuất hiện trong lúc train**.

### Vì sao per-class recall quan trọng hơn accuracy trung bình

Con số 0.548 nếu đứng một mình sẽ gây hiểu nhầm là model "khá đều" trên cả 5 lớp.
Nhìn vào recall từng lớp thì thấy không phải:

- **lying = 0.284** — chỉ nhỉnh hơn đoán mò (0.20 cho bài toán 5 lớp) một chút.
- **sitting = 0.469, standing = 0.551** — không hề thấp; standing gần đúng bằng
  mức trung bình.
- **walking = 0.646, running = 0.782** — cao hơn hẳn trung bình.

Vậy model không tệ đều: nó **rất kém ở đúng một lớp** (lying), khá ở hai lớp tĩnh
còn lại, và tốt ở hai lớp động. Đây chính là manh mối dẫn thẳng đến Section 2 —
lỗi có cấu trúc rõ ràng, không phải nhiễu ngẫu nhiên.

Ma trận nhầm lẫn xác nhận điều đó (hàng = nhãn thật, cột = dự đoán):

```
        lying  sitting standing walking running
lying     957      580     1517     283      36
sitting   881     1583      800      95      15
standing  666      708     1860     116      23
walking   256      334      456    2181     147
running   131       51      151     406    2647
```

Toàn bộ khối nhầm lẫn nặng nằm gọn trong góc trên-trái 3×3 (lying/sitting/standing
lẫn lộn với nhau), còn walking/running gần như không bị lẫn sang nhóm tĩnh.

---

## 2. Root cause (B) — vì sao lại như vậy?

### 4 đặc trưng thực sự đo cái gì

Tất cả 4 đặc trưng được tính trên **một cửa sổ trượt ~2.4 giây**
(`WINDOW_SIZE = 60` mẫu ở `IMU_HZ = 25`), trượt mỗi 0.4 giây (`STRIDE_SIZE = 10`)
— **không phải** trên cả hiệp vận động 90 giây. 🔧 *(Đây là chỗ hiểu sai trong
bản nháp gốc: "trung bình của cả hiệp vận động". Một hiệp 90s sinh ra hàng trăm
dòng dữ liệu, mỗi dòng là một cửa sổ 2.4s, chứ không phải một dòng cho cả hiệp.)*

| Đặc trưng | Đo gì (trong cửa sổ 2.4s) |
| :--- | :--- |
| `mean_mag` | Độ lớn gia tốc trung bình |
| `std_mag` | Độ biến thiên của gia tốc — tín hiệu "rung" nhiều hay ít |
| `peak_max` | Gia tốc mạnh nhất xuất hiện trong cửa sổ |
| `peak_rel` | `peak_max / mean_mag` — mức độ "gai góc": đỉnh vượt trung bình bao nhiêu lần |

`peak_rel` lớn nghĩa là có một cú thay đổi gia tốc đột ngột trong 2.4s đó. Chỉ số
này thiên về bài toán **fall detection** (phát hiện té ngã) hơn là phân biệt tư
thế — ở bài toán hiện tại nó không đóng góp nhiều.

### Cơ chế: magnitude bất biến với phép xoay

Magnitude được tính là:

```
mag = sqrt(ax² + ay² + az²)
```

Đây chính là **độ dài (norm) của vector gia tốc**. Khi thiết bị bị xoay — người
đeo lật cổ tay, hoặc đeo lệch góc — phép xoay chỉ đổi **hướng** của vector chứ
không đổi **độ dài** của nó. Từng thành phần `ax`, `ay`, `az` thay đổi giá trị,
nhưng tổng `sqrt(ax²+ay²+az²)` giữ nguyên.

Hệ quả trực tiếp: cả 4 đặc trưng — đều là hàm của magnitude — **không mang bất kỳ
thông tin nào về hướng (orientation)**, chỉ phản ánh cường độ chuyển động.

Ghép với bản chất của 5 hoạt động:

- **lying / sitting / standing** khác nhau ở **orientation** (góc của cổ tay so
  với phương trọng lực), gần như không khác nhau ở **năng lượng chuyển động** —
  đúng chính xác phần mà bộ đặc trưng này bị mù.
- **walking / running** khác nhau ở **năng lượng chuyển động** — đúng phần mà
  magnitude *đo được*.

Bằng chứng số (`check_accel_variance_by_activity.py`): median `std_mag` ở nhóm
tĩnh = **23.3** so với nhóm động = **365.0** — chênh **15.7 lần**. Khoảng cách đó
thừa sức tách tĩnh khỏi động. Nhưng nhìn vào bên trong nhóm tĩnh:

| Hoạt động | median `std_mag` | std (độ trải) |
| :--- | ---: | ---: |
| sitting | 17.6 | 65.6 |
| standing | 25.3 | 64.8 |
| lying | 31.9 | 95.5 |
| *walking* | *269.1* | *157.4* |
| *running* | *1410.2* | *662.0* |

Ba tư thế tĩnh **có** lệch nhau chút ít về median (17.6 → 31.9), nhưng độ trải
của mỗi lớp (65–95) lớn hơn nhiều lần khoảng cách giữa các median đó — nghĩa là
ba phân phối chồng lên nhau gần như hoàn toàn, không có ngưỡng nào cắt được.
Ngược lại, khoảng cách tĩnh → walking → running lớn hơn hẳn độ trải, nên cắt
ngưỡng dễ dàng. Đây là dạng số của đúng kết luận toán học ở trên.

**Kết luận nhân quả:** đây là **giới hạn cấu trúc của bộ đặc trưng**, không phải
lỗi chọn hyperparameter hay thiếu dữ liệu. Không có cách chỉnh model nào cứu được
một thông tin đã bị xoá ngay từ bước tính đặc trưng.

### Ba lần thử sửa bằng đặc trưng per-axis và vì sao đều thất bại

**Cách 1 — Raw device-frame (dùng thẳng trục x/y/z của thiết bị).** Ý tưởng: giá
trị từng trục cho biết hướng thiết bị, từ đó suy ra người đang nằm sấp / ngửa /
nghiêng — thông tin mà magnitude đã xoá mất.

🔧 *Giả thuyết ban đầu là "3 hoạt động đều có những trường hợp lật cổ tay giống
nhau nên trục bị lẫn". Số liệu thật bác bỏ giả thuyết này:* đặc trưng raw
per-axis mean đạt **68.2% ở N = 4**, nhưng riêng **P03 rớt còn 46.8%** (ngang
baseline). Nếu cơ chế đúng là "lật cổ tay trong lúc vận động", nó phải làm hỏng
**đều tất cả participant** — thực tế chỉ một người hỏng, ba người còn lại vẫn
tốt. Cơ chế thật nhiều khả năng là **mỗi người đeo thiết bị ở một góc cố định
khác nhau** (khác nhau *giữa người*, không phải lật *trong lúc* đo): cùng một
giá trị trục thô ứng với những góc thực tế khác nhau ở mỗi người, nên model học
được từ 17 người không áp được sang người thứ 18. Đây đúng là hiện tượng
**wearing-angle confound** đã ghi trong CHANGELOG.md (2026-07-22 → 2026-07-28).

> ⚠️ *Điểm còn cần xác nhận:* giả thiết trên dựa vào việc participant **không**
> được yêu cầu đeo theo một hướng cố định. Cần kiểm tra lại giao thức thu dữ
> liệu thực tế trước khi khẳng định chắc trong bản nộp.

**Cách 2 — Baseline-relative (chuẩn hoá theo mức nền của từng người).** Ý tưởng:
thu một hoạt động tĩnh nhất (lying) trong khoảng đủ dài (10–15 phút để cơ thể ổn
định), lấy đó làm mốc 0 riêng cho từng người, rồi phân loại dựa trên độ chênh so
với mốc đó.

Không áp dụng được cho dataset hiện tại vì giao thức chỉ dành **1 phút 30 giây**
cho mỗi hoạt động — quá ngắn để có một mức nền ổn định. Một hướng thay thế
(**window-relative**) được đề xuất trong Section 5, nhưng chưa được kiểm chứng.

**Cách 3 — Rotation-augmented (nhân dữ liệu bằng cách xoay giả lập).** Ý tưởng:
90 giây mỗi hoạt động là ít dữ liệu, nên sinh thêm mẫu bằng cách xoay dữ liệu
hiện có sang nhiều hướng đeo khác nhau.

Thất bại vì nó giải sai bài toán: 3 lớp tĩnh khó phân biệt là do **giống nhau về
gia tốc**, chứ không phải do thiếu đa dạng hướng đeo. Thêm nữa, trong lúc thu
dữ liệu participant luôn để tay ngang hoặc duỗi thẳng — hướng đeo có đổi thì chủ
yếu đổi giữa trục x và y, còn trục z (trục dọc theo phương trọng lực ở tư thế đó)
gần như không đổi. Xoay giả lập quanh một trục vốn không biến thiên thì không
sinh thêm thông tin gì mới.

---

## 3. Solution (C)

**Thay đổi đã thực hiện:** gộp 3 lớp tĩnh (lying / sitting / standing) thành một
lớp `stationary`, đưa bài toán từ 5 lớp về **3 lớp** (stationary / walking /
running).

**Giữ nguyên tuyệt đối mọi thứ khác:** cùng `DecisionTreeClassifier(max_depth=5,
min_samples_leaf=5)`, cùng 4 đặc trưng, cùng 18 participant, cùng giao thức
LOGO-CV. Chỉ đổi cột nhãn: `label` → `activity_group`.

| Lớp | Recall (3-class) |
| :--- | ---: |
| stationary | 0.951 |
| walking | 0.632 |
| running | 0.777 |
| **Mean accuracy** | **0.853** |

### Vì sao đây là lựa chọn hợp lệ, không phải "chọn thước đo đẹp"

Lý do nằm ở chỗ nó nối thẳng với cơ chế đã chỉ ra ở Section 2, chứ không phải thử
nhiều cách chia nhãn rồi giữ cách nào ra số cao nhất:

1. Section 2 đã chứng minh bộ đặc trưng này **về mặt toán học không thể** phân
   biệt 3 tư thế tĩnh (magnitude bất biến với phép xoay).
2. Việc gộp loại bỏ **đúng phần** mà bộ đặc trưng không quan sát được, và **giữ
   nguyên** phần nó quan sát được (khác biệt về năng lượng chuyển động giữa
   tĩnh / walking / running).
3. Ranh giới gộp được suy ra **trước** khi nhìn kết quả, từ nguyên nhân gốc —
   không phải suy ngược từ accuracy.

Ngoài ra, `max_depth=5` được giữ nguyên có chủ đích: chỉ 4 đặc trưng và 18
participant là tập dữ liệu nhỏ, để cây rẽ nhánh tự do sẽ overfit theo từng người
và làm hỏng chính giá trị mà LOGO-CV đang đo.

**Điều báo cáo này không tuyên bố:** việc gộp lớp **không** làm model phân biệt
được lying/sitting/standing. Thông tin đó vẫn mất — chỉ là bài toán đã được định
nghĩa lại cho đúng với năng lực đo đạc thực tế của phần cứng hiện tại.

---

## 4. Quantified improvement — cải thiện này có ý nghĩa không?

### Effect size so với baseline tầm thường

Chạy `check_majority_baseline.py` trên chính `data/processed/master_dataset.csv`
để biết một model "ngu" nhất — luôn đoán lớp đông nhất — sẽ được bao nhiêu.
Baseline được tính trên **đúng 16.880 dòng** mà model được train/đánh giá (đã
loại dòng chuyển tiếp), vì baseline tính trên tập dòng khác thì không so được với
accuracy:

| | Majority-class baseline | LOGO-CV accuracy | Biên hơn baseline |
| :--- | ---: | ---: | ---: |
| 5-class | **0.201** (dataset gần cân bằng, ≈ random 1/5 = 0.200) | 0.548 | **+0.347** |
| 3-class | **0.599** (`stationary` gộp 3/5 lớp gốc nên chiếm đa số) | 0.853 | **+0.254** |

**Đây là điểm quan trọng nhất của section này:** so thẳng 0.548 → 0.853 (+0.305)
là **phóng đại mức cải thiện**. Một phần lý do 0.853 cao là vì bài toán 3 lớp
**dễ hơn về mặt cấu trúc** — chỉ cần đoán "stationary" cho mọi trường hợp đã đúng
59.9%, do việc gộp đã tạo ra một lớp chiếm 3/5 dữ liệu.

Thước đo công bằng là biên vượt baseline **của chính bài toán đó**:

- 5-class: hơn baseline **+0.347** (gấp 2.7 lần baseline)
- 3-class: hơn baseline **+0.254** (gấp 1.4 lần baseline)

Nghĩa là: bài toán 3 lớp cho **accuracy tuyệt đối cao hơn và dùng được hơn**,
nhưng **phần "model thực sự học được"** thì lại nhỏ hơn so với bài toán 5 lớp.
Cải thiện là thật, nhưng nhỏ hơn con số +0.305 thô gợi ý.

### Tính công bằng của phép so sánh

Phép so sánh này là apples-to-apples: **giữ nguyên** dataset (18 participant),
model, hyperparameter, bộ đặc trưng, và giao thức LOGO-CV. **Chỉ đổi** cột nhãn.
Vì vậy chênh lệch quan sát được quy được về đúng một nguyên nhân — độ khó của
việc định nghĩa nhãn — chứ không lẫn với hiệu ứng của model hay dữ liệu.

### Ý nghĩa thực tiễn

Cần thành thật ở điểm này: **project hiện chưa định nghĩa một ứng dụng downstream
cụ thể nào**, nên chữ "dùng được" ở đây mang tính giả định.

- **3-class ở 0.853** đủ tin cậy cho ứng dụng chỉ cần phân biệt "đang nghỉ" vs
  "đang vận động" — ví dụ activity-aware logging, hoặc chuyển chế độ tiết kiệm
  pin khi người dùng ở trạng thái tĩnh. Nó cũng đủ ổn định để làm demo thời gian
  thực (hiển thị nhãn hoạt động trực tiếp trên web app).
- **5-class ở 0.548, với lying ở 0.284** thì **chưa** đủ cho bất kỳ ứng dụng nào
  cần phân biệt chính xác 3 tư thế tĩnh — ví dụ theo dõi tư thế nằm/ngồi/đứng cho
  mục đích sức khoẻ. Ở mức recall đó, nhãn `lying` gần như không mang thông tin.

---

## 5. Suggestion for further improvement

Mọi hướng dưới đây đều xuất phát từ cùng một kết luận ở Section 2: **thông tin về
orientation đã bị xoá ở bước tính đặc trưng**, nên muốn tiến xa hơn thì phải bổ
sung một kênh đo *mới*, chứ không phải chỉnh model.

Nguyên tắc chung cho mọi lần thu tới: **thu raw đủ 6 trục (accel + gyro) trước,
xử lý trên máy tính sau.** Ba lần thử per-axis vừa rồi đều bị giới hạn vì chỉ có
4/18 participant có raw capture.

### Plan 1 — Gyroscope + calibration step (phương án đầy đủ)

- **Cách làm:** đọc thêm 3 trục gyro (MPU6050 đã có sẵn, hiện chưa đọc), và thêm
  một bước calibration đầu mỗi phiên: participant giữ một tư thế tham chiếu vài
  giây, thiết bị ghi lại làm mốc 0 riêng cho người đó.
- **Vì sao có thể ăn ở chỗ 3 lần trước thua:** cả 3 lần trước đều thiếu đúng một
  mốc tham chiếu, nên cùng một giá trị trục thô lại ứng với góc thực tế khác nhau
  ở mỗi người (wearing-angle confound ở Section 2). Một mốc calibrate theo từng
  người về nguyên tắc loại bỏ đúng nhiễu loạn đó.
- **Chi phí:** phải sửa firmware (log gyro), sửa giao thức thu (thêm bước
  calibration), và **thu lại toàn bộ từ đầu** — 18 participant hiện có không
  retrofit được vì không ai có dữ liệu gyro lẫn calibration.

**Đánh giá riêng:** hướng này đúng về logic nhưng là phương án **tốn nhất**. Nếu
phải chọn một, mình chọn Plan 2 trước.

### Plan 2 — Chia hai tầng model (phương án rẻ hơn, ưu tiên)

Thay vì một model 5 lớp duy nhất, tách thành hai model theo đúng ranh giới mà
Section 2 đã chỉ ra:

- **Tầng 1 — phân biệt tĩnh / walking / running:** giữ nguyên decision tree +
  4 đặc trưng magnitude hiện tại. Phần này đã chạy tốt (recall 0.632 / 0.777),
  không cần đụng tới.
- **Tầng 2 — bên trong nhóm tĩnh, phân biệt lying / sitting / standing:** dùng
  trục **gyro** để bắt **chuyển động đổi tư thế** (ví dụ nằm → ngồi có một đoạn
  xoay rõ rệt trên gyro dù magnitude gia tốc gần như không đổi), thay vì cố
  phân biệt bằng gia tốc tĩnh.

**Vì sao rẻ hơn Plan 1:** không cần bước calibration riêng cho từng người — chỉ
cần đọc thêm gyro, tức là đổi phần firmware đọc cảm biến chứ không đổi giao thức
thu dữ liệu.

**Rủi ro cần nói thẳng:** nếu participant giữ nguyên tư thế hoàn toàn (không có
đoạn chuyển), gyro sẽ không cho tín hiệu gì để phân biệt. Nghĩa là Plan 2 phân
biệt được *sự chuyển tư thế*, chưa chắc phân biệt được *tư thế đang giữ*. Chỉ
benchmark thật mới trả lời được — không đưa ra con số kỳ vọng trước.

Hệ quả cho giao thức thu: **đoạn chuyển tiếp giữa các hoạt động chính là dữ liệu
có giá trị nhất** cho Plan 2, chứ không phải phần thừa cần cắt bỏ (xem phần Phụ
lục).

### Plan 3 — Body acceleration (BA), phác thảo, chưa kiểm chứng

Hướng thứ ba: tách gia tốc đo được thành thành phần trọng lực và thành phần
chuyển động cơ thể (body acceleration), rồi phân nhánh theo tần số trội và góc
so với vector trọng lực:

```
              [ Dữ liệu Body Acceleration (BA) ]
                             |
                Kiểm tra Tần số (Dominant Freq)
                          /     \
                 (Dải thấp)     (Dải cao)
                      /             \
           [ VUNG TAY NHẸ ]     [ VUNG TAY MẠNH ]
                      |                |
        Kiểm tra Góc Hình Học     Kiểm tra Góc Hình Học
          (ba_gravity_angle)        (ba_gravity_angle)
             /         \               /         \
         (~90°)   (~0°/180°)       (~90°)   (~0°/180°)
           /           \             /           \
    [ ĐỨNG IM ]  [ NGỒI IM ]  [ ĐỨNG VUNG ]  [ NGỒI VUNG ]
```

Sơ đồ trên mới là phác thảo cây quyết định dự kiến, **chưa chạy trên dữ liệu
thật** — cần raw 6 trục mới kiểm chứng được. Nó bổ trợ cho Plan 2 chứ không thay
thế: `ba_gravity_angle` là cách khai thác thông tin orientation *tĩnh*, còn gyro
khai thác thông tin *chuyển tiếp*.

### Ý tưởng window-relative — CHƯA KIỂM CHỨNG, không trình bày như phương pháp đã chốt

Vì baseline-relative (Section 2, cách 2) cần 10–15 phút mà giao thức chỉ có 90
giây, một hướng thay thế là tính **mức nền tĩnh cục bộ ngay trong cửa sổ 90s**
đó, rồi dùng độ lệch so với mức nền làm chỉ số "độ hỗn loạn":

```
Độ lệch = accel_hiện_tại − mức_nền_tĩnh_tạm_thời
```

Giả thuyết: độ lệch thấp (tín hiệu phẳng) → sitting; độ lệch cao, nhiều đỉnh
nhọn → standing (đứng lâu thì phải dịch trọng tâm chân, sinh ra gia tốc đột
biến). Kèm thêm đặc trưng `dominant-axis` (trục x/y/z nào có |giá trị| lớn nhất)
để tách lying khỏi sitting/standing.

> ⚠️ **Trạng thái: chưa validate.** Có một câu hỏi mở chưa trả lời được, và nó
> có thể phủ định cả ý tưởng: với một tư thế **tĩnh** (không có chuyển động
> trong cửa sổ), việc trừ đi mức nền cục bộ có đồng thời trừ luôn **thành phần
> trọng lực không đổi** — thứ duy nhất phân biệt được lying/sitting/standing —
> hay không? Nếu có, phép biến đổi này xoá đúng tín hiệu mà nó cần. Phải trả lời
> câu hỏi này (và xác nhận lại giả thiết hướng đeo ở Section 2) trước khi đưa
> vào như một đề xuất thật.

### Benchmark plan

Thu lại raw 6 trục (accel + gyro) trên nhóm participant mới, dùng **đúng giao
thức LOGO-CV hiện tại** để so sánh được trực tiếp, và đối chiếu:

- (a) Plan 2 — model hai tầng (gyro cho nhóm tĩnh, decision tree hiện tại cho
  nhóm động)
- (b) baseline hiện tại — 0.548 ở 5 lớp

Báo cáo theo **per-class recall của 3 lớp tĩnh**, không chỉ accuracy tổng — vì
đó mới là phần đang hỏng. Không đưa ra con số kỳ vọng trước khi có dữ liệu thật.

### Một quan sát thêm từ per-class recall

Ở bài toán 3 lớp, `stationary` đạt 0.951 trong khi walking (0.632) và running
(0.777) thấp hơn hẳn — phần accuracy còn thiếu tập trung ở hai lớp động, không
phải ở lớp tĩnh đã gộp. Một giả thuyết đáng ghi lại (chưa kiểm chứng): phần
chênh này đến từ khác biệt **sinh lý và thói quen vận động giữa từng người** —
sải chân, nhịp bước, cách vung tay khi đi và chạy khác nhau rõ giữa các
participant. Nếu đúng, hướng khai thác là **cá nhân hoá ngưỡng phân loại cho
người dùng mới** thay vì dùng chung một ngưỡng cho tất cả. Kiểm chứng được bằng
cách xem phương sai accuracy giữa 18 fold LOGO-CV — hiện đang trải từ 0.559
(P06) đến 0.991 (P15), một khoảng rất rộng, nhất quán với giả thuyết này.

---

## Phụ lục — Rút kinh nghiệm cho lần thu dữ liệu sau

*(Đây là bài học về quy trình, không phải finding — nên đưa vào CHANGELOG.md chứ
không tính là kết quả nghiên cứu.)*

1. **Chừa thời gian đệm giữa các hoạt động (~20s)** để participant chuyển tư thế,
   và lọc bỏ 10–15 giây đầu mỗi đoạn khi xử lý. Lưu ý ngược lại: nếu thu được
   gyro thì **chính đoạn chuyển tiếp này lại là keypoint** để phân biệt
   lying/sitting/standing (Plan 2) — nên phải **ghi lại nó** rồi mới tách ra,
   không được bỏ ngay từ lúc thu.
2. **Vẽ trước cây quyết định cho các tình huống dữ liệu có thể xảy ra**, trước
   khi thu. Khi đi vào một nhánh mà tắc thì bỏ nhánh đó sớm và sang nhánh khác,
   thay vì phát hiện ra sau khi đã thu xong toàn bộ.
3. **Luôn thu đủ raw 6 trục** kể cả khi chưa chắc sẽ dùng. Cả 3 lần thử per-axis
   đều bị giới hạn vì chỉ có raw capture cho 4/18 participant.
4. **90 giây/hoạt động là đủ** cho việc train activity classifier — không cần
   quãng 10–15 phút. Trade-off phải nói rõ: nhịp tim chưa kịp ổn định trong 90
   giây, nên độ dài này đủ cho subsystem A nhưng chưa chắc đủ cho phần PPG/HR.

---

## Reproducibility checklist

- [x] Chạy lại `train_activity_classifier.py` từ đầu đến cuối và ra đúng 2 con số
      (0.548, 0.853) — **đã xác nhận ngày 2026-08-13**.
- [x] Chạy lại `check_majority_baseline.py` và ra đúng 0.201 / 0.599 —
      **đã xác nhận ngày 2026-08-13**.
- [ ] Đọc hiểu từng dòng đủ để giải thích khi advisor hỏi — đặc biệt Section 4
      (phép so sánh biên vượt baseline) và 3 chỗ đánh dấu 🔧 ở Section 2.
- [ ] Xác nhận lại giao thức thu dữ liệu: participant có được yêu cầu đeo thiết
      bị theo một hướng cố định không? (ảnh hưởng trực tiếp đến lập luận
      wearing-angle confound ở Section 2)
- [ ] Đối chiếu báo cáo với rubric thật của môn học — Claude không có quyền truy
      cập rubric và không thể xác nhận phần này.
