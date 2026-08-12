# Adaptive Filter Comparison (Subsystem B) — Outline (fill in yourself)

This is a skeleton, not a draft. Sections have prompts + the raw, verified numbers/
facts you can cite — the explanation/reasoning/writing is yours to do. Source for
every number below: `lms_denoise_mvp.py` (run it yourself, re-verify before citing).
A full Claude-written reference draft with the same numbers exists at
`adaptive_filter_comparison_2026-07-28_CLAUDE_REFERENCE.md` — use it to check you
haven't mis-transcribed a number, not as text to copy from.

---

## 1. Research question (given)

On ESP32-class hardware under FreeRTOS memory and CPU constraints, which adaptive
filter algorithm (LMS, RLS, or Wiener) best removes motion artifacts from wrist-worn
PPG — and does it achieve clinically usable heart rate accuracy?

---

## 2. Setup — facts to restate in your own words

- 5 participants have complete dual-channel PPG (fingertip + dorsal-wrist MAX30102)
  + synchronized 3-axis accelerometer: P02, P03, P04, P16, P17. One ~7.5-min session
  each, 5 activities (lying, sitting, standing, walking, running), fixed order.
- Ground truth: fingertip PPG, bandpassed 0.7-3.5 Hz (42-210 bpm), BPM estimated per
  8s sliding window (2s stride) via dominant FFT frequency, with a continuity
  constraint (window's pick restricted to within 25 bpm of previous estimate,
  5-window median-seeded init).
- Filters compared, all using bandpassed 3-axis-accel magnitude as a single
  reference signal, 8-tap FIR: Baseline (no filtering), NLMS, RLS (with a
  covariance-reset safeguard — an earlier version without it diverged numerically
  during low-motion portions), Wiener (batch/non-adaptive, ridge-regularized normal
  equations, solved once per session).
- Metric: MAE in bpm between each filter's windowed BPM estimate and fingertip
  ground truth, pooled and broken out by participant/activity.

Your job: explain *why fingertip PPG is a reasonable ground truth here* and *why
the continuity constraint on the FFT estimator matters* (what goes wrong without
it — see CHANGELOG.md 2026-07-28 entries for the naive-peak-counting failure mode
that motivated it).

---

## 3. Results — raw numbers (verified, reproducible from `lms_denoise_mvp.py`)

**Pooled MAE across all 5 participants, all windows (bpm):**

| Filter | MAE (bpm) |
| :--- | ---: |
| Baseline (no filtering) | 26.95 |
| NLMS | 26.96 |
| RLS | 29.83 |
| Wiener | 29.96 |

**Per-participant MAE (bpm), best filter marked \*:**

| Participant | Baseline | NLMS | RLS | Wiener |
| :--- | ---: | ---: | ---: | ---: |
| P02 | 29.58 | **24.04\*** | 30.51 | 27.91 |
| P03 | 27.79 | 29.94 | **25.21\*** | 27.23 |
| P04 | **21.64\*** | 18.48 | 46.06 | 47.43 |
| P16 | 33.95 | 26.48 | **26.42\*** | 26.57 |
| P17 | 21.78 | 35.86 | 20.96 | **20.67\*** |

**By activity, pooled across participants (bpm):**

| Activity | Baseline | NLMS | RLS | Wiener |
| :--- | ---: | ---: | ---: | ---: |
| Lying | 26.82 | 20.53 | 34.41 | 22.83 |
| Sitting | 18.95 | 27.12 | 21.90 | 32.06 |
| Standing | 26.16 | 29.43 | 30.67 | 25.51 |
| Walking | 34.38 | 22.77 | 24.51 | 28.71 |
| Running | 28.53 | 35.38 | 38.33 | 41.29 |

---

## 4. Finding (A) — is there a winner?

Prompt: state the headline result plainly. Look at the pooled table AND the
per-participant table together — do they tell the same story? (Hint: is the
"best filter" the same participant to participant?) Explain why reporting only
the pooled number would be misleading here, the same way section 1 of the
activity-classifier report explains why the 5-class average hides per-class
recall.

---

## 5. P04 outlier investigation — root cause (B), partially resolved

Facts:
- P04 is a strong outlier for RLS/Wiener specifically (46-47 bpm MAE vs 18-22 bpm
  for baseline/NLMS).
- P04 has the highest correlation between wrist PPG and the accelerometer
  reference of any participant (r = -0.72; others range -0.13 to 0.35).
- P03 has a similarly high correlation (r = -0.47) but does NOT fail nearly as
  badly with RLS/Wiener.

Your job: propose a mechanism connecting high PPG-accelerometer correlation to
RLS/Wiener failing (why would a tighter, closer-to-exact adaptive fit remove real
PPG signal along with the artifact, when the two are correlated?), and explicitly
state why the P03 counter-example means this is NOT a confirmed root cause — just
a plausible, unconfirmed one. Don't overclaim more than the data supports.

---

## 6. Negative result — triaxial reference channels

Facts:
- Using the 3 accelerometer axes as separate reference channels (24 taps total)
  instead of collapsing to magnitude (8 taps) was tested, on the hypothesis that
  magnitude discards directional coupling information.
- It made every filter substantially worse: NLMS 26.96→37.44, RLS 29.83→37.65,
  Wiener 29.96→35.41 bpm pooled MAE.
- ~45,000 noisy samples available per session.

Your job: explain *why* 24 parameters vs 8 would overfit at that sample count (a
parameters-to-samples argument), and state the practical conclusion (single-
channel magnitude reference should be the default until per-session data volume
is much larger — do you agree, and would you quantify "much larger"?).

---

## 7. Limitations — facts to weigh, argument is yours

- N=5 is small for a definitive claim either way.
- Single ~7.5-minute session per participant — no test-retest, no longer-duration
  stability test.
- Ground truth (fingertip-derived) is not clinical-grade (e.g. ECG) — MAE numbers
  are relative comparisons between filters under one ground-truth method, not
  absolute clinical accuracy figures.
- Filter length fixed at 8 taps across all 3 algorithms for comparability, not
  tuned per algorithm.
- Single reference signal (accel magnitude), single hyperparameter setting per
  filter (NLMS step size, RLS forgetting factor, Wiener regularization) — not
  swept or tuned per participant.

Your job: which of these limitations, if any, do you think could *plausibly flip*
the null result if fixed (vs. which are unlikely to matter)? Pick at least one and
justify your reasoning — don't just list them.

---

## 8. Framing / conclusion — is the null result itself a finding?

Prompt: given sections 4-7, write your own concluding framing. Consider: is "no
filter beats no-filtering, at N=5, on ESP32-class hardware with single-reference
classical adaptive filters" a defensible and useful negative result? What would
make it more or less convincing to your advisor? How does it compare to how
published wrist-PPG work is typically evaluated (commercial hardware, richer
multi-sensor references) — and does that comparison strengthen or weaken your
claim?

---

## Reproducibility checklist (for you to verify before submitting)

- [ ] Can you re-run `lms_denoise_mvp.py` top to bottom and get the same pooled
      MAE numbers (26.95 / 26.96 / 29.83 / 29.96)?
- [ ] Do you understand every line well enough to explain it if your advisor asks?
- [ ] Have you checked this outline/report against your class's actual rubric —
      Claude does not have access to that and cannot confirm this meets it
