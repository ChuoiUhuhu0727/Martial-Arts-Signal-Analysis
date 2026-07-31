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

---

## Reproducibility checklist (for you to verify before submitting)

- [ ] Can you re-run `train_activity_classifier.ipynb` top to bottom and get the same
      2 numbers (0.548, 0.853)?
- [ ] Do you understand every line well enough to explain it if your advisor asks?
- [ ] Have you checked this outline/report against your class's actual rubric —
      Claude does not have access to that and cannot confirm this meets it
