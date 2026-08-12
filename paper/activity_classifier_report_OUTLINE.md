# Activity Classifier Finding — Outline (fill in yourself)

This is a skeleton, not a draft. Sections have prompts + the raw, verified numbers you
can cite -- the explanation/reasoning/writing is yours to do. Source for every number
below: `train_activity_classifier.ipynb` (run it yourself, re-verify before citing).

---

## 1. Finding (A)

Prompt: state the headline result plainly, with the exact evaluation protocol (so a
reader can judge whether it's trustworthy).

Numbers available to cite:
- 5-class (lying/sitting/standing/walking/running) LOGO-CV mean accuracy: **0.548**
- N = 18 participants, leave-one-participant-out cross-validation
- Per-class recall: lying **0.283**, sitting **0.490**, standing **0.548**, walking
  **0.639**, running **0.771** (from `train_activity_classifier.py` output / notebook)

Your job: explain *what LOGO-CV means* and *why per-class recall matters more than
overall accuracy here* (i.e. why hiding behind the 0.548 average would be misleading).

Your answer:
Logo-cv means leave one group out. Khác với cách chia train/test thông thường, mỗi
participant sẽ lần lượt bị cho ra rìa và biến thành test set để kiểm tra model có học
vẹt không. Cứ lặp lại như thế cho đến khi tất cả participant trong dataset đều 1 lần
được làm test set. Logo-cv chia dữ liệu dựa trên nhãn định danh (participant), khác
với cross-validation thông thường chia dữ liệu theo dòng ngẫu nhiên.

Per-class recall quan trọng hơn accuracy trung bình ở đây vì: 0.283 (lying) cao hơn
đoán mò (0.20 cho 5-class) nhưng chỉ hơn một chút, và thấp hơn hẳn 0.548 — con số
average mà báo cáo dùng làm đại diện. Trong khi đó sitting (0.490) và standing (0.548)
không hề thấp — standing thậm chí bằng đúng average. Vậy model không tệ đều: chỉ riêng
lying là thấp hẳn, gần như đoán mò, còn 2 lớp còn lại trong nhóm stationary vẫn ở mức
tương đương average. Nếu chỉ đọc con số 0.548, người đọc sẽ nghĩ model "khá đều" trên
cả 5 lớp — nhưng thực tế lying đang gần với đoán mò, bị che khuất bởi average.

---

## 2. Root cause (B) — why does this happen?

Prompt: explain the mechanism, not just "the model is bad". What do the 4 features
(`mean_mag`, `std_mag`, `peak_rel`, `peak_max`) actually measure? What property of
lying/sitting/standing makes them hard to tell apart *given that specific measurement*?

Things you already worked out in this session that you can build the explanation from
(don't just copy these sentences — restate them in your own words, this is the part
that shows you understand it):
- All 4 features are derived from accelerometer **magnitude**
- Magnitude is invariant to rotation (a mathematical fact — restate why, in your own
  words, ideally with the formula)
- lying/sitting/standing differ from each other only in *orientation*, not in motion
  energy
- walking/running differ in motion *energy* (magnitude variance), which magnitude-based
  features CAN see — that's why those 2 classes are fine

Evidence you can point to: `check_accel_variance_by_activity.py` output — median
`std_mag` static ≈ 24 vs dynamic ≈ 362 (dynamic/static ratio ≈ 15x). This is why
walking/running are distinguishable but lying/sitting/standing are not, using the same
feature set.

Optional (if you want to strengthen this section): mention that 3 earlier attempts to
fix this with per-axis features (raw device-frame, baseline-relative, rotation-
augmented) were tried and did not generalize across participants (see CHANGELOG.md,
2026-07-22 through 2026-07-28 entries) — briefly explain *why* (wearing-angle
confound), don't just say "it didn't work".

Your answer — what the 4 features measure:
- mean_mag: sức mạnh trung bình của gia tốc trong 1 cửa sổ thời gian (~2.4s —
  `WINDOW_SIZE=60` mẫu @ `IMU_HZ=25`, trượt mỗi 0.4s), không phải cả hiệp vận động
  (~90s).
- std_mag: độ chênh lệch (biến thiên) của gia tốc trong cùng cửa sổ 2.4s đó.
- peak_max: gia tốc mạnh nhất trong cửa sổ 2.4s đó.
- peak_rel = peak_max / mean_mag: tỉ lệ giữa đỉnh và trung bình trong cùng cửa sổ
  2.4s — đo mức độ "gai góc" của tín hiệu trong cửa sổ đó. Nếu số này lớn, nghĩa là
  có một thay đổi gia tốc đột ngột trong 2.4s đó — chỉ số này hợp với fall detection
  hơn, không dùng cho mục đích đó ở bài toán này.

Tại sao magnitude bất biến với rotation: magnitude = sqrt(ax² + ay² + az²) chính là
độ dài (norm) của vector gia tốc. Khi thiết bị bị xoay (đổi hướng đeo), phép xoay chỉ
đổi *hướng* của vector, không đổi *độ dài* của nó — nên dù từng thành phần ax, ay, az
riêng lẻ thay đổi giá trị theo hướng xoay, tổng sqrt(ax²+ay²+az²) vẫn giữ nguyên. Đó
là lý do mean_mag/std_mag/peak_max/peak_rel — đều là hàm của magnitude — không mang
thông tin về hướng đeo (orientation), chỉ phản ánh cường độ chuyển động.

Your answer — tại sao 3 lần thử per-axis trước không generalize:

*Alternative 1 — Raw device-frame (thay vì Earth Frame):* tận dụng số liệu trục xyz
ứng với hướng thiết bị để biết người đeo đang nằm sấp/ngửa/nghiêng. Không phù hợp vì
raw device-frame nhạy cảm với việc lật cổ tay — 3 hành động lying/sitting/standing
đều có những trường hợp lật cổ tay giống nhau, nhất là khi 4 chỉ số đang dùng đều là
magnitude nên giá trị các trục đã bù trừ lẫn nhau.
Đối chiếu với số liệu thật: raw per-axis mean đạt 68.2% ở N=4, nhưng riêng P03 rớt
còn 46.8% (ngang baseline). Nếu cơ chế là "lật cổ tay giống nhau giữa 3 hành động"
như hypothesis ban đầu, nó phải ảnh hưởng **đều tất cả participant** — nhưng thực tế
chỉ P03 fail, 3 người còn lại vẫn đạt 68.2%. Vậy bác bỏ hypothesis lật cổ tay; cơ chế
thật sự nhiều khả năng là mỗi người đeo thiết bị ở một góc *cố định* khác nhau —
khác nhau *giữa người*, không phải lật cổ tay *trong lúc* vận động — đúng với mô tả
"wearing-angle confound" đã ghi trong CHANGELOG.

*Alternative 3 — Rotation-augmented:* 3 class khó phân biệt (lying/sitting/standing)
là do acceleration magnitude giống nhau, không phải do hướng đeo trục xyz. Trong lúc
thu data, participants luôn để tay ngang hoặc duỗi thẳng — nên hướng đeo có đổi thì
cũng chỉ đổi giữa trục x và y, còn trục z (dọc theo hướng trọng lực khi tay ở tư thế
đó) không đổi. → Nếu làm lại: dùng body acceleration (BA) thay vì raw axis.

---

## 3. Solution (C)

Prompt: what did you change, and why does it follow logically from the root cause in
section 2 (not just "we tried this and it worked")?

Numbers available to cite:
- 3-class (stationary/walking/running) LOGO-CV mean accuracy: **0.853**
- Per-class recall: stationary **0.951**, walking **0.632**, running **0.777**
- Same model (`DecisionTreeClassifier(max_depth=5, min_samples_leaf=5)`), same 4
  features, same 18-participant dataset, same LOGO-CV protocol as section 1 — only the
  target column changed (`label` → `activity_group`)

Your job: explain why this is a valid methodological move and not "cherry-picking a
metric that looks better" — i.e., connect back to section 2's mechanism explicitly.

Your answer:
Input data chỉ có 4 feature (mean_mag, std_mag, peak_rel, peak_max) và dataset chỉ có
18 participant — một tập dữ liệu khá nhỏ, dễ overfit nếu để decision tree rẽ nhánh quá
sâu; đó là lý do giữ `max_depth=5, min_samples_leaf=5` thay vì để cây tự do phát triển.

Việc gộp 3 lớp thành `stationary` không phải cherry-pick vì nó nối thẳng với cơ chế đã
chỉ ra ở Section 2: cả 4 feature đều là hàm của magnitude, mà magnitude bất biến với
rotation nên không phân biệt được lying/sitting/standing (chỉ khác nhau ở orientation,
không khác ở motion energy) — đây là giới hạn *cấu trúc* của bộ feature, không phải
lỗi ngẫu nhiên có thể sửa bằng cách chọn nhãn khác. Gộp 3 lớp đó lại thành 1 loại bỏ
đúng phần mà bộ feature này *không thể* phân biệt được, còn giữ nguyên phân biệt giữa
3 nhóm còn lại (stationary/walking/running) — nơi magnitude *có* khác biệt rõ (do khác
nhau ở motion energy, thứ magnitude đo được). Vì vậy 0.548 → 0.853 phản ánh đúng việc
loại bỏ 1 giới hạn đã root-cause được, chứ không phải chọn một cách chia nhãn ngẫu
nhiên tình cờ cho ra số đẹp hơn.

---

## 4. Quantified improvement — is it meaningful?

Prompt: state the before/after, and argue (don't just assert) whether the improvement
is meaningful. Consider:
- Effect size: 0.548 → 0.853 (+0.305). Is that large relative to what a trivial
  baseline would get? (What would a majority-class or random baseline score, for 5-class
  vs 3-class? You can compute this yourself from the class distribution in
  `data/processed/master_dataset.csv`.)
- Fairness of comparison: is it a fair apples-to-apples comparison? (What's held
  constant? What changed? Section 3 already answered this — reuse it.)
- Practical significance: does 0.853 cross into a range that's actually usable for
  something (e.g. a real-time demo, a downstream application)? For what?

Your answer:

**Effect size (computed via `check_majority_baseline.py`, not guessed):**

| | Majority-class baseline | LOGO-CV accuracy | Margin over baseline |
| :--- | ---: | ---: | ---: |
| 5-class | 0.201 (dataset gần cân bằng, ngang random 1/5=0.200) | 0.548 | +0.347 |
| 3-class | 0.599 (`stationary` gộp 3/5 lớp gốc, nên chiếm đa số) | 0.853 | +0.254 |

So sánh thẳng 0.548 vs 0.853 (+0.305) hơi đánh lừa: một phần con số 0.853 cao là vì
bài toán 3-class *dễ hơn do cấu trúc* (chỉ cần đoán "stationary" cho mọi trường hợp đã
đúng 59.9% rồi), không hoàn toàn vì model học tốt hơn. Thước đo công bằng hơn là margin
trên baseline riêng của từng bài toán: 5-class hơn baseline +0.347, 3-class hơn baseline
+0.254 — 3-class vẫn hơn baseline rõ rệt (gấp ~1.4 lần baseline của chính nó), nhưng
biên độ cải thiện thực chất **nhỏ hơn** con số +0.305 thô cho thấy.

**Fairness of comparison:** giữ nguyên dataset, cùng model, cùng protocol LOGO-CV. Thứ
thay đổi là gộp 3 lớp có magnitude/chỉ số gần giống nhau (lying/sitting/standing) thành
1 lớp `stationary`, để lại 3 lớp có khác biệt magnitude rõ rệt (stationary/walking/
running) — đúng như Section 3 đã giải thích.

**Practical significance:** hiện project chưa có 1 downstream application cụ thể được
định nghĩa (không phải fall-detection, không phải power-mode switching cụ thể nào),
nên "usable" ở đây mang tính giả định. Với biên độ recall như hiện tại — stationary
0.951, walking 0.632, running 0.777 — 3-class đủ tin cậy cho một ứng dụng chỉ cần phân
biệt "đang nghỉ" vs "đang vận động" (ví dụ: activity-aware logging, hoặc chuyển chế độ
tiết kiệm năng lượng khi stationary). 5-class ở 0.548, với lying gần đoán mò (0.283),
thì **chưa** đủ tin cậy cho bất kỳ ứng dụng nào cần phân biệt chính xác 3 tư thế tĩnh
(ví dụ: theo dõi tư thế nằm/ngồi/đứng cho mục đích sức khỏe).

---

## 5. Suggestion for further improvement

Prompt: propose a concrete next step to improve on the CURRENT ceiling (either push
5-class accuracy up, or push 3-class higher, or both) — with a method, an honestly
uncertain expected effect (do not invent a projected accuracy number you can't back
up), and a specific benchmark plan.

Starting material from this session (restate in your own words, and decide if you
agree with the reasoning or want to argue something different):
- Idea: add gyroscope (3-axis, present on the MPU6050 hardware but not currently read)
  + a calibration step at the start of each session (participant holds a reference
  posture briefly; device records it as a per-person zero-reference)
- Why this might work where the 3 earlier per-axis attempts didn't: those attempts had
  no calibration reference, so the same raw axis reading meant a different real-world
  angle for different people's wearing angle — a per-person calibrated reference
  removes that confound in principle
- Cost/constraints to mention: requires firmware changes (log gyro), protocol change
  (add calibration step), and full re-collection (can't retrofit onto the 18 already-
  collected participants — none have gyro or calibration data)
- Benchmark plan: same LOGO-CV protocol, on a NEW dataset collected with gyro+
  calibration, compared against the current 0.548 5-class baseline as the reference
  point

You decide: do you find this proposal convincing? Is there a cheaper alternative you'd
propose instead? This section should reflect your own judgment, not just relay the idea
above.

**Moved here from Section 2 (was misplaced — this is a new untested proposal, not an
explanation of a past attempt):** "window-relative" idea — instead of a per-participant
baseline (which failed, session too short at 90s to get a stable 10-15min baseline),
compute a local floor over the current 90s window and use deviation from that floor as
a "chaos index" (thấp = sitting, cao/nhiều đỉnh nhọn = standing), plus a `dominant-axis`
feature (which of x/y/z has largest |value|) to separate lying from sitting/standing.
**Status: NOT validated, do not present as a decided methodology.** Open question raised
mid-session, not yet answered: for a *static* posture (no motion within the window), does
subtracting a nearby-window floor also subtract the constant gravity-orientation offset
that's the *only* thing distinguishing lying/sitting/standing — i.e. does this erase
the exact signal it needs? Also depends on the still-unconfirmed "does everyone wear the
watch in the same orientation" fact-check (pending, see project memory). Resolve both
before including this as a real proposal.

Your answer — is the gyro+calibration proposal (given above) convincing, cheaper
alternative:

Proposal trên (gyro + calibration step, full re-collection) hợp lý về mặt logic — vì 3
lần thử per-axis trước đều thiếu 1 tham chiếu để "zero" hướng đeo của từng người, và
calibration step giải quyết đúng thiếu sót đó. Nhưng đây là phương án tốn nhất (đổi cả
firmware, protocol, và phải thu lại từ đầu — 18 participant hiện có không dùng lại được).

Alternative rẻ hơn — chia model thành 2 lớp thay vì 1 model 5-class duy nhất:
- **Lớp "động" (walking/running):** giữ nguyên decision tree + 4 feature hiện tại (đã
  hoạt động tốt — recall 0.639/0.771 ở 5-class, 0.632/0.777 ở 3-class) — không cần sửa.
- **Lớp "tĩnh" (lying/sitting/standing):** dùng trục gyro (đã có sẵn trên MPU6050,
  chưa đọc) để bắt chuyển động *đổi tư thế* (VD: nằm→ngồi có 1 đoạn xoay rõ rệt trên
  gyro, dù magnitude accel không đổi nhiều) thay vì dựa vào accel magnitude tĩnh.

Vì sao rẻ hơn: không cần calibration step riêng biệt cho mỗi người — chỉ cần đọc thêm
gyro (đổi phần cứng đọc, không đổi protocol thu). Rủi ro: gyro trong lúc đứng yên hoàn
toàn (không đổi tư thế) có thể không cho tín hiệu gì để phân biệt — cần benchmark thực
tế mới biết, không giả định trước con số.

**Benchmark plan:** thu lại raw 6-trục (accel + gyro) cho các participant mới, dùng
đúng LOGO-CV protocol như hiện tại, so 2 hướng: (a) model 2 lớp (gyro cho tĩnh, decision
tree cũ cho động) so với (b) baseline hiện tại (0.548 5-class). Không đưa ra con số kỳ
vọng trước khi có data thật.

Insight thêm từ per-class recall (0.548→0.853): phần "mất" 0.2 accuracy còn lại (0.853
chưa phải 1.0) nhiều khả năng đến từ khác biệt sinh lý/thói quen vận động giữa các
participant (physiology) — hướng tận dụng: cá nhân hoá ngưỡng phân loại cho user mới
thay vì dùng 1 ngưỡng chung cho tất cả.

Ghi chú thu thập cho lần thu data tiếp theo (nên đưa vào CHANGELOG.md, không phải report
này — đây là process lesson, không phải finding):
- Chèn thêm thời gian đệm (~20s) giữa các hoạt động để participant chuyển tư thế, và
  lọc bỏ 10-15s đầu của mỗi đoạn khi xử lý — đúng đoạn chuyển tiếp này lại là keypoint để
  phân biệt lying/sitting/standing nếu thu được gyro.
- Vẽ trước cây quyết định/các nhánh dữ liệu có thể xảy ra trước khi thu, để biết nhánh
  nào tắc thì bỏ sớm thay vì phát hiện sau khi đã thu xong.
- Luôn thu đủ raw 6 trục (accel + gyro) kể cả khi chưa chắc dùng — 3 lần thử per-axis
  trước đều bị giới hạn vì chỉ có raw capture cho 4/18 participant.

---

## Reproducibility checklist (for you to verify before submitting)

- [ ] Can you re-run `train_activity_classifier.ipynb` top to bottom and get the same
      2 numbers (0.548, 0.853)?
- [ ] Do you understand every line well enough to explain it if your advisor asks?
- [ ] Have you checked this outline/report against your class's actual rubric —
      Claude does not have access to that and cannot confirm this meets it
