# Week 12 Report — Finalising the dataset and redefining the problem

## What this week was about — the overview

**Phase:** Phase 3 — *Polish and Documentation* (Weeks 10–13).

**In one sentence:** finalising the dataset at **18 participants**, and finding that simply
**redefining the problem to match what the sensor can do** raises accuracy from 54.8% to
**85.3%**.

**Why it matters:** this follows directly from the Week 9 discovery. Once it is known that
the current sensor *cannot in principle* separate the three still postures, the right
response is not more model tuning — it is **asking whether the problem is stated correctly**.

---

## Group 1 — Finalising the dataset

- **Adding an 18th participant**, distinct from the test session rejected in Week 11.
  → Final dataset: **18 people**.

## Group 2 — Merging the three still postures

![Figure 12.1: The three still postures merged into one "at rest" group. This is not picking whichever split scores best, but redefining the problem to match what the sensor measures.](figures_en/week12_regroup.png)

- **Everything else held absolutely constant, only the grouping changed** (~07-30): same
  model, same four features, same dataset, same marking scheme. Only lying, sitting and
  standing were merged into one "at rest" group.

| Problem | Accuracy | "At rest" correctly identified |
| :--- | ---: | ---: |
| 5 classes | 54.8% | — |
| **3 classes** | **85.3%** | **95.1%** |

### Is merging classes just picking a split that scores better?

This is the most important question to answer, because from the outside it looks a lot like
trying many splits and keeping whichever scores highest.

**It is not**, for two reasons:

1. **The merge boundary was derived before looking at the result**, from the root cause
   proven in Week 9: all four features are functions of acceleration magnitude, and
   magnitude does not change when the wrist rotates. The three still postures differ exactly
   there. This is a **structural** limit of the feature set, not a matter of luck.
2. **The merge removes exactly the part the features cannot observe**, while keeping the
   part they observe very well — the difference in movement intensity between rest, walking
   and running.

→ **What this means:** the jump from 54.8% to 85.3% reflects **removing a limit whose cause
is understood**, not a lucky experiment.

**What this does not claim:** merging classes does **not** make the model able to tell lying
from sitting from standing. That information is still lost. The problem has simply been
redefined to match what the current hardware can actually measure.

## Group 3 — Deciding to report both numbers

- **Keeping the five-class figure as the headline, with three-class as an accompanying
  result** (~07-30).
  → **What this means:** the five-class version is less accurate but still carries
  information about the three still postures, which has more practical value for the end
  application. Both are reported with an explanation, rather than showing only the prettier
  number.

- **Drafting the skeletons of the two reports** for the project's two tracks, as raw
  material for Week 13.

---

## Where things stood at the end of the week

| Item | Result |
| :--- | :--- |
| Final dataset | 18 participants |
| Headline figure | 5 classes — 54.8% |
| Accompanying result | 3 classes — 85.3% |

## How this differed from the original plan

The original plan said *"External user testing and final iteration"* — testing with people
entirely outside the project. Not done: all current participants are people known to or
near the team.

**Which thesis chapter this feeds:** Chapter 3 section 3.5 (redesign and fair evaluation
against a baseline).

---
[← Week 11](week_11.md) · [Weekly reports index](README.md) · [Week 13 →](week_13.md)
