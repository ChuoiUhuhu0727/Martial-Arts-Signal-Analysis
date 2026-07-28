# Adaptive Filter Comparison for Wrist-Worn PPG Motion Artifact Removal — Preliminary Results

Status: MVP-phase result, ready to incorporate into the Q3 journal draft. Not a final
result — see Limitations.

## Research Question

On ESP32-class hardware under FreeRTOS memory and CPU constraints, which adaptive
filter algorithm (LMS, RLS, or Wiener) best removes motion artifacts from wrist-worn
PPG — and does it achieve clinically usable heart rate accuracy?

## Methods

**Participants.** 5 of the project's participants have complete dual-channel PPG
(simultaneous fingertip + dorsal-wrist MAX30102) and synchronized 3-axis
accelerometer capture: P02, P03, P04, P16, P17. Each contributed one ~7.5-minute
session covering 5 activities (lying, sitting, standing, walking, running) under a
fixed-order protocol.

**Ground truth.** Fingertip PPG (known to give a clean signal, minimal motion
coupling) is bandpassed to the plausible heart-rate band (0.7-3.5 Hz / 42-210 bpm),
then BPM is estimated per 8-second sliding window (2s stride) via the dominant
frequency in a windowed FFT, with a continuity constraint across windows (each
window's frequency pick is restricted to within 25 bpm of the previous window's
estimate, with a 5-window median-seeded initialization) to prevent the estimator
from locking onto the PPG waveform's own harmonics. This method was chosen after a
naive peak-counting approach was found to produce physiologically implausible
instantaneous BPM swings; see `CHANGELOG.md` (2026-07-28 entries) for the full
iteration history.

**Filters compared**, all using bandpassed 3-axis-accelerometer magnitude as a
single reference signal, 8-tap FIR:
- **Baseline**: no filtering — the wrist PPG channel as captured.
- **NLMS**: normalized least-mean-squares adaptive noise canceller.
- **RLS**: recursive least squares (matrix-inversion-lemma update), with a
  covariance-reset safeguard (trace(P) capped) — an earlier version without this
  diverged numerically during the low-motion portions of each session.
- **Wiener**: batch (non-adaptive) optimal FIR filter, solved once per session via
  the normal equations over the whole recording, ridge-regularized.

**Metric.** Mean absolute error (MAE) in bpm between each filter's windowed BPM
estimate (same windowing/tracking method as ground truth, applied to the filter's
residual) and the fingertip ground truth, pooled and broken out by
participant/activity.

Implementation: `lms_denoise_mvp.py`. Reproducible top to bottom from the raw
per-participant capture files.

## Results

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

## Finding

**No filter shows a consistent advantage over doing nothing, at N=5.** Baseline and
NLMS are essentially tied pooled (26.95 vs 26.96 bpm); RLS and Wiener are slightly
worse pooled. Per participant, the best-performing filter is different every time —
no single algorithm dominates.

**One partial explanation investigated**: participant P04 is a strong outlier for
RLS/Wiener specifically (46-47 bpm MAE vs 18-22 bpm for baseline/NLMS). P04 also has
the highest correlation between the wrist PPG signal and the accelerometer reference
of any participant (r=-0.72, vs -0.13 to 0.35 for the others) — a plausible
mechanism is that RLS/Wiener's tighter, closer-to-exact fit removes real PPG signal
along with motion artifact when the two are strongly correlated, while NLMS's
slower, gradient-based adaptation is more conservative. However, P03 has a similarly
high correlation (r=-0.47) without failing nearly as badly, so this is not a
confirmed root cause — flagged for future investigation, not resolved here.

**One negative result**: using the 3 accelerometer axes as separate reference
channels (24 taps total) instead of collapsing to a single magnitude channel (8
taps) was tested on the hypothesis that magnitude discards directional coupling
information. It made every filter substantially worse (NLMS 26.96→37.44, RLS
29.83→37.65, Wiener 29.96→35.41 bpm pooled MAE), likely because 24 parameters
overfit the ~45,000 noisy samples available per session. Single-channel magnitude
reference should be kept as the default until per-session data volume is much
larger.

## Limitations

- **N=5** is small for a definitive claim either way — the per-participant variance
  observed (no consistent best filter) could resolve differently with more
  participants.
- **Single ~7.5-minute session per participant.** No test of longer-duration
  stability or of a different session on the same person (test-retest).
- **Ground truth itself has an MAE ceiling.** The fingertip-derived ground truth,
  while validated against the on-device wrist BPM estimate and bug-checked, is not
  a clinical-grade reference (e.g. ECG). All MAE numbers above should be read as
  relative comparisons between filters under one ground-truth method, not absolute
  clinical accuracy figures.
- **Filter length fixed at 8 taps**, chosen for comparability across the 3
  algorithms rather than tuned per algorithm. RLS/Wiener in particular might behave
  differently at other tap counts.
- **Single reference signal (accelerometer magnitude) and single set of
  hyperparameters** (NLMS step size, RLS forgetting factor, Wiener regularization)
  — not swept or tuned per participant.

## Suggested framing for the paper

Given the above, a defensible framing is: *"On this ESP32-class hardware with
single-reference, fixed-length classical adaptive filters, we did not observe a
consistent motion-artifact-removal benefit at N=5 — a negative/null result that
itself has value, since most published wrist-PPG artifact-removal work is
evaluated on commercial hardware (Apple Watch, Empatica, Garmin) with more
sophisticated multi-sensor references, not microcontroller-class devices under
RTOS constraints with a single low-cost IMU."* This directly answers the research
question as originally posed (README.md, Research Track section) without
overclaiming a filter recommendation the data doesn't support.
