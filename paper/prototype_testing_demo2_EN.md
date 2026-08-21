# Prototype Testing Demonstration 2

**Wrist-worn activity and heart rate device — Prototype testing report**

Wearable Activity & Health Monitor · Subsystem: Firmware & AI

---

## 1. The prototype under test, and the test conditions

### 1.1. The prototype

A complete wrist-worn device, running on battery, with all processing done on the chip:

| Component | Configuration |
| :--- | :--- |
| Microcontroller | Seeed XIAO ESP32-S3, running FreeRTOS with multiple tasks |
| Motion sensor | MPU6050 — 3-axis accelerometer, sampled at 25 Hz |
| Optical sensor | MAX30102 on the back of the wrist, reflective mode, 940 nm infrared LED |
| Reference sensor | MAX30102 clipped to the fingertip (test equipment only, not part of the product) |
| Storage | On-chip flash, written continuously through each session |
| On-device AI model | Decision Tree exported to C, running directly on the chip |

*Table 1: The prototype configuration put under test.*

### 1.2. Realistic test conditions

Testing was **not** carried out under ideal laboratory conditions. The device was worn on
real people's wrists, powered by battery, with no cable to a computer during the session.

| Factor | Condition applied |
| :--- | :--- |
| Participants | **18 people** for activity recognition; 5 with both optical channels |
| Session length | ~7.5 minutes continuous, no pauses |
| Activities | 5 real movement states: lying, sitting, standing, walking, running |
| Power | LiPo battery, no cable |
| Data transfer | Written to on-chip memory; Bluetooth only for monitoring |
| Disturbance | Participants' spontaneous movements were not restricted |

*Table 2: Test conditions.*

One constraint shaped the whole test design: **each participant is measured only once**.
There is no repeat session. This forced the test procedure to catch faults **during the
measurement**, not afterwards during analysis.

---

## 2. Testing procedures

The prototype was tested at **three independent levels**, each catching a class of fault the
others cannot see.

### 2.1. Level 1 — Testing the collection protocol

![Figure 1: The structure of one session. 15 seconds of preparation, five activities of 90 seconds each, with changeover gaps that are excluded from analysis.](weekly_reports_en/figures_en/week06_protocol_timeline.png)

Every session follows a fixed sequence so that the data label always comes from the protocol
timer, never from a human judgement or a model output.

**Checks during the measurement itself:** two indicators are shown live to the operator —
whether the sensor is properly against the skin, and how many seconds remain in the current
activity.

### 2.2. Level 2 — Testing the model on data, independently of the user

![Figure 2: In each evaluation round, one person is held out entirely as the test; the model may only learn from the other 17. Repeated for all 18 rounds.](weekly_reports_en/figures_en/week09_logocv.png)

The model is evaluated with **LOGO-CV (Leave-One-Group-Out Cross-Validation)** — holding out
one whole person as the test set while the model learns from the other 17, repeated for all
18 rounds.

**Why this method:** if the data were split randomly by row, neighbouring time windows from
the same person would land in both the training and the test set. The model could then score
highly just by remembering that individual — a very pretty number that means nothing, because
in practice the device always meets new users. LOGO-CV gives the **real number for a
stranger**.

### 2.3. Level 3 — Testing on the real hardware

![Figure 3: The three steps for getting the model from laptop onto the chip. The step of connecting the new model to the running program was once missed, and only surfaced when it was loaded onto the device.](weekly_reports_en/figures_en/week11_train_to_device.png)

The model trained on a laptop is exported to C, loaded onto the chip, and then **worn on a
wrist and run live**. This is the only level that catches faults introduced by moving from
laptop to hardware.

### 2.4. Metrics used

| Metric | Used for | Why it was chosen |
| :--- | :--- | :--- |
| LOGO-CV accuracy | Activity recognition | Measures performance on new users, not on people already learned |
| Per-class recall | Activity recognition | A single average hides where the specific failure is |
| Majority-class baseline | Activity recognition | Without a floor, an accuracy figure carries no meaning |
| MAE (bpm) | Heart rate | The required metric under the ANSI/AAMI EC13 standard |
| Signal yield rate | Heart rate | Before discussing error, we must know how often a signal is readable at all |
| Physiological check | Validating the reference data | Heart rate while running must be higher than while lying still |

*Table 3: Six metrics and the reason for each.*

---

## 3. Key performance results

### 3.1. Activity recognition subsystem

| Configuration | Accuracy (LOGO-CV, 18 people) | Note |
| :--- | ---: | :--- |
| 5 classes (lying/sitting/standing/walking/running) | 54.8% | The originally committed configuration |
| **3 classes (at rest/walking/running)** | **85.3%** | After redefining the problem, see section 6.1 |

Per-class recall in the five-class configuration shows the error is **not evenly spread**:

| Activity | Recall | Assessment |
| :--- | ---: | :--- |
| Lying | 28.4% | Close to random guessing (20%) |
| Sitting | 46.9% | Heavily confused with standing |
| Standing | 55.1% | Heavily confused with sitting |
| Walking | 64.6% | Clearly separated from the still group |
| Running | 78.2% | Fully separated |

*Table 4: Per-class recall — all of the error concentrates on the three still postures.*

**Live results on the device** (worn on a wrist, classifying in real time):

| Activity | Correct when running live |
| :--- | ---: |
| Running | **99%** |
| Standing | **76%** |
| Lying / Sitting | Still confused with standing |

*Table 5: Live results on the hardware.*

The important point: **the pattern of confusion in the live test matches exactly what was
predicted during training.** This confirms the whole chain *train → export → load onto
device* works correctly, with no new error introduced by integration.

### 3.2. Heart rate subsystem

![Figure 4: The share of time in which the signal actually contains a readable heartbeat. Moving from the fingertip to the wrist loses almost three quarters of the information.](figures_en/hr_coverage_by_signal.png)

| Signal | Share of windows with a valid heart rate |
| :--- | ---: |
| Fingertip (reference channel) | 35.0% |
| **Wrist, unfiltered** | **9.6%** |
| Wrist + NLMS | 8.0% |
| Wrist + RLS | 5.5% |
| Wrist + Wiener | 12.7% |

*Table 6: Signal yield rate — the most important figure for this subsystem.*

The conclusion does not depend on the chosen acceptance threshold. Sweeping the full range
from loose to strict: the more the signal is required to carry a genuinely physiological
rhythm, the further the wrist yield falls — at the strictest setting it is just **1.6%**
against the fingertip's 19.6%, a gap of **12.2 times**.

---

## 4. Verification against the project requirements

| Requirement from the proposal | Test result | Status |
| :--- | :--- | :--- |
| Dataset of ≥ 10 participants | 18 people | **Exceeded** |
| Wrist vs fingertip controlled experiment, ≥ 5 people | Exactly 5, both channels complete | **Met** |
| Activity recognition ≥ 85% on unseen users | 3 classes reach 85.3%; 5 classes reach 54.8% | **Met, conditionally** |
| Five-class classification — required deliverable | Reduced to three classes | Changed, with measured justification |
| Usable real-time heart rate | Signal yield 9.6% | **Not met** |
| Model running directly on the microcontroller | Yes, verified on a person's wrist | **Met** |

*Table 7: Test results against the project requirements.*

**On the "met, conditionally" row:** the 85% threshold is reached, but on a problem narrowed
from five classes to three. This report does not present that as an unqualified success — the
reason for narrowing it, and the evidence behind that decision, are in sections 5.1 and 6.1.

---

## 5. Issues identified through testing

All four issues below **surfaced only because of testing**, and three of the four had passed
every automated check beforehand.

### 5.1. Issue 1 — The three still postures cannot be separated (a structural limit)

**Found by:** breaking recall down per class (Table 4), then tracing the cause with a
mathematical argument.

![Figure 5: Raw acceleration of all five activities on the same scale. The three still postures are three nearly flat lines, indistinguishable by eye and by number.](figures_en/waveform_by_activity.png)

All four features fed to the model are computed from the **magnitude** of acceleration, that
is `√(ax² + ay² + az²)` — the **length** of the acceleration vector. When the wrist rotates,
the vector changes **direction** but **not length**. And lying, sitting and standing differ
precisely in wrist direction.

Direct numerical evidence: the median `mean_mag` for lying / sitting / standing / walking is
**2000 · 1828 · 1896 · 1937** — four completely different body positions, yet almost identical
acceleration magnitudes, all around 1g, meaning the sensor is only measuring **gravity**.

→ **Conclusion:** this is a **structural limit of the feature set**, not a bad parameter
choice. The necessary information is erased at the feature extraction step, before the model
sees the data. No amount of model tuning can recover it.

### 5.2. Issue 2 — Six sessions with nobody wearing the device

**Found by:** plotting the raw signal and comparing it against physical expectation.

![Figure 6: An automatic rule scanned all 21 sessions. The six rejected ones were equipment tests — they had passed every automated check beforehand.](weekly_reports_en/figures_en/week08_quality_gate.png)

Six sessions had the right number of labels, the right number of rows, and no errors in the
log — but the device was lying still on a table with nobody wearing it. They only surfaced
when somebody plotted the signal and asked: *why is the "running" segment as flat as the
"lying" one?*

→ **Severity:** had these six reached the training set, the model would have been taught that
running looks like lying still. Every later number would have been wrong, with no way to trace
the source.

### 5.3. Issue 3 — The reference measurement was wrong by a factor of two

**Found by:** the physiological check — *is the heart rate higher while running than while
lying down?*

![Figure 7: Heart rate from the fingertip reference channel by activity. This channel fails the physiological check for 3 of the 5 participants.](figures_en/gt_sanity_by_activity.png)

The fingertip reference channel — assumed to be a clean standard — **fails the check for 3 of
5 people**. The worst case recorded **127.7 bpm while standing still but only 89.7 bpm while
running**.

Tracing the cause by plotting the raw signal and counting peaks by hand: the waveform was
**very clean**, with 30 peaks in 12 seconds, that is 155.6 bpm, while the algorithm reported
**77.0 bpm** — exactly half.

The competing explanation was ruled out: if each beat were being counted twice, the gaps
between peaks would alternate long-short. The measured ratio of odd to even gaps was **1.03**
(perfectly even), while the ratio of odd to even peak heights was **2.22**. So it is the
**height** that alternates, not the spacing.

→ **The mechanism:** alternating tall and short beats make the waveform repeat only every
*two* beats, creating a strong spectral component at exactly half the true rate. The algorithm
locked onto that.

→ **Why it survived so long:** the fault occurs in the measurement layer, but the guard against
implausible values sits in the smoothing layer. When the measurement layer kept returning
[77, 77, 77, …], perfectly consistent, the smoothing layer trusted it completely; when the
measurement layer occasionally caught the true 156, the smoothing layer **rejected it**. The
system actively protected the wrong number.

### 5.4. Issue 4 — The wrong optical wavelength for the measurement site

**Found by:** the signal yield results after the reference was corrected (Table 6).

| Wavelength | Absorption by haemoglobin | Suited to |
| :--- | :--- | :--- |
| ~525 nm (green) | **Very strong** | Reflective measurement at the wrist — what commercial watches use |
| 660 nm (red) | Weak | SpO2, transmissive measurement at the fingertip |
| 940 nm (infrared) | Weak | SpO2, transmissive measurement at the fingertip |

*Table 8: Optical absorption of each wavelength.*

The MAX30102 emits only red and infrared — two wavelengths that blood barely absorbs. At the
wrist they penetrate deeply, but most of the returning light comes from deep tissue, tendon
and bone, so the pulse is only a very small ripple on a large background.

→ **Conclusion:** this is *"the right sensor at the wrong anatomical site"*. The wrist position
is not the mistake — commercial watches use it too. The mistake is the **wavelength**.

---

## 6. Improvements made based on the testing outcomes

Every improvement below was triggered by a specific test result, not by prior judgement.

| # | Improvement | Triggered by | Result after the change |
| :--- | :--- | :--- | :--- |
| 1 | 15 seconds of preparation before the first activity; prompt sound moved to the laptop | Labels wrong in the first seconds of each session | Labels match reality from the start |
| 2 | Continuous skin-contact checking instead of once at startup | Sensor shifting mid-session unnoticed | Detected during the measurement |
| 3 | Beat-detection threshold adapting to each person | Heart rate frozen for tens of seconds | Continuous measurement, no dead spots |
| 4 | Automatic rule rejecting sessions with nobody wearing the device | Issue 2 (section 5.2) | 6 of 21 sessions correctly rejected |
| 5 | Removing the rule that forced "lying" when the device was still | Testing on real hardware | The new model performs its main function |
| 6 | **Redefining the problem from five classes to three** | Issue 1 (section 5.1) | **54.8% → 85.3%** |
| 7 | **Replacing the heart rate estimator (v2)** | Issue 3 (section 5.3) | Passing the physiological check: **2/5 → 4/5 people** |

*Table 9: Seven improvements, each traceable to the test result that triggered it.*

### 6.1. Improvement 6 in detail — Redefining the problem

![Figure 8: The three still postures merged into one group. This is not picking whichever split scores better, but redefining the problem to match what the sensor measures.](weekly_reports_en/figures_en/week12_regroup.png)

The model, the four features, the dataset and the evaluation protocol were all held
absolutely constant — only the three still postures were merged into one group.

**Is this picking a split that scores better?** No, for two reasons:

1. **The merge boundary was derived before looking at the result**, from the root cause in
   section 5.1.
2. **The merge removes exactly the part the feature set cannot observe**, while keeping the
   part it observes very well.

**A fair evaluation — comparison against the floor:**

| Problem | Floor (always guess the largest class) | Measured accuracy | Margin over the floor |
| :--- | ---: | ---: | ---: |
| 5 classes | 0.201 | 0.548 | **+0.347** |
| 3 classes | 0.599 | 0.853 | **+0.254** |

*Table 10: Fair comparison against each problem's own floor.*

→ **Recorded honestly:** comparing 54.8% with 85.3% directly **overstates the improvement**.
The three-class problem is structurally easier because the "at rest" class covers 60% of the
data. The fair measure is the margin over each problem's own floor — and by that measure, the
part the model **actually learned** in the three-class problem (+0.254) is **smaller** than in
the five-class problem (+0.347).

### 6.2. Improvement 7 in detail — Replacing the heart rate estimator

The new estimator changes three things: it takes the **median gap between beats** in the time
domain instead of following a spectral peak; it **returns "not readable"** when the beats are
too irregular instead of guessing; and it **removes the cross-window continuity constraint**
entirely.

| Verification case | Old estimator | New estimator | Counted by hand |
| :--- | ---: | ---: | ---: |
| Participant A running | 77.0 | **156.9** | 155.6 |
| Participant B running | 155.8 | **118.9** | 111.3 |
| Passing the physiological check | 2/5 | **4/5** | — |

*Table 11: Verifying the new estimator against manual peak counting.*

The new estimator corrects the error **in both directions** — one case was being read at half,
the other at double. This confirms it works from the real physics of the pulse, not from a
one-directional adjustment that happened to land close.

---

## 7. How the testing outcomes changed the project's direction

The original proposal asked: *which noise-removal algorithm — LMS, RLS or Wiener — best
removes motion artifacts from wrist PPG?*

The test results in section 3.2 show that **the premise of this question does not hold**. For
about 90% of the time, the wrist signal in the current hardware configuration contains no
heartbeat to clean up. A filter *separates* signal from noise — it does not *create* signal.

This is why the project shifted its focus from **optimising algorithms** to **tracing a
hardware limit**. That shift was not a matter of preference; it was a **direct consequence of
the test results**:

| If the original direction continued | What the test results show |
| :--- | :--- |
| Tuning the three filters' parameters | All three make things worse, by subtracting the little signal that remains |
| Trying a fourth filter | Does not change the fact that the input contains no heartbeat |
| Adding more participants | Does not change the optical properties of the wavelength |

*Table 12: Why continuing the original direction would not solve the problem.*

The final outcome of the heart rate subsystem is therefore a **carefully validated negative
result**: software filters cannot compensate for choosing the wrong optical wavelength at the
sensing layer. The original hypothesis — *cheap hardware plus good algorithms can substitute
for specialised hardware* — was **rejected experimentally**, not abandoned.

---

## 8. Lessons from the testing process

Three of the four issues in section 5 **passed every automated check** and were only found by
a physical check:

| Issue | What the metric said | The reality | Found by |
| :--- | :--- | :--- | :--- |
| Six fake sessions | "Right labels, right rows, no errors" | Nobody wearing the device | Plotting the raw signal |
| Three still postures | "54.8% accuracy — a mediocre model" | The feature set is blind to three classes | A three-line mathematical argument |
| Reference off by half | "MAE around 27 bpm — the filters are useless" | The ruler itself was wrong by half | Asking "is running higher than lying?" |

*Table 13: Three faults that passed every automated check.*

All three faults were **numerically consistent** — the sequence [77, 77, 77, …] is very
steady; the confusion matrix is very stable across 18 evaluation rounds. That consistency is
exactly what let them pass every automated check: metrics verify whether the data **agrees
with itself**, not whether the data **agrees with physical reality**.

**The principle drawn from this:** every reference signal needs at least one test against a
known physical or physiological law. The three tests that found these faults each took **under
15 minutes**, and all three sat outside every automated evaluation pipeline.

---

## 9. Index of supporting evidence

| Type of evidence | Content | Location |
| :--- | :--- | :--- |
| Measurement data | 18 participants, 20,258 data windows (16,880 after excluding changeovers) | `data/processed/master_dataset.csv` |
| Raw data | Six-channel raw signal for the 5 participants with both optical channels | `experiments/wrist/valid_sessions/` |
| Test log | Status of every session, including those rejected and why | `experiments/wrist/session_manifest.csv` |
| Test code | 12 scripts; every number reproducible with one command | See `paper/EVIDENCE_GUIDE.md` |
| Measurement plots | 11 plots generated directly from the data, none drawn by hand | `paper/figures/` |
| Firmware source | The feature computation running on the device | `firmware_ble/main.cpp`, lines 738–750 |

*Table 14: Index of evidence.*

**Reproducibility:** every script fixes `random_state = 0`, so there is no randomness. Running
them any number of times gives exactly the same result. The procedure for reproducing each
number is documented in `paper/EVIDENCE_GUIDE.md`.

**Evidence not included:** this report does not include photographs or video of the hardware
testing session. The live results in Table 5 are recorded as data logs, not as a recording.

---

## 10. Conclusion

The prototype was tested under realistic conditions on 18 participants, at three independent
levels: the collection protocol, user-independent model evaluation, and live operation on the
hardware.

**Requirements met:** the activity recognition subsystem reaches 85.3% on users it has never
seen, runs directly on the microcontroller, and its results on real hardware match those on
the laptop.

**Requirements not met:** the heart rate subsystem, with the cause traced to the hardware
layer — the wrong optical wavelength for reflective measurement at the wrist.

**The value of the testing process:** four issues were identified, three of which had passed
every automated check and surfaced only through physical verification. Seven improvements were
made, each traceable to the test result that triggered it. Most importantly, testing revealed
that a result which appeared finished had actually been measured with a broken ruler — and
this was corrected before it reached the final conclusions.
