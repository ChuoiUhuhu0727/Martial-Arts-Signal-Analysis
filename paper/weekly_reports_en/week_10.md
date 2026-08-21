# Week 10 Report — Comparing three noise-removal methods for the heart signal

> ⚠️ **THIS WEEK'S CONCLUSION WAS LATER OVERTURNED — see [Week 13](week_13.md)**
>
> The four numbers published this week were measured against a heart rate derived from the
> fingertip sensor. On 15 August that reference channel was found to be **wrong by a factor
> of two for 3 of the 5 participants** because of an algorithm fault, so all four numbers
> were measured with **a bent ruler** and cannot be used to draw a conclusion.
>
> This week's content is **kept as it was, not rewritten**. A confident conclusion later
> overturned by the team itself is part of the research process, and is direct evidence for
> the argument in Chapter 5 section 5.3 of the thesis.

## What this week was about — the overview

**Phase:** Phase 3 — *Polish and Documentation* (Weeks 10–13). Matches milestones **M4**
and **M5** in the plan.

**In one sentence:** building and running the project's **separate research track** — a
comparison of three noise-removal algorithms to see which measures wrist heart rate best.

**Why it matters:** this is the *research* part, as distinct from the *product* part.
Activity recognition (Weeks 5–9) is a feature users can see. This part answers an open
question that nobody has answered on hardware this cheap.

---

## How the experiment was set up

![Figure 10.1: The wrist signal is mixed with movement noise. All three algorithms use the motion sensor to guess the noise and subtract it, then the result is compared against the fingertip reading.](figures_en/week10_filter_setup.png)

All three algorithms rest on the same idea: **the wrist signal = the real heartbeat + noise
from movement**. Use the motion sensor to guess the noise, then subtract it. They differ
only in how they make the guess.

## Group 1 — Fixing the measuring tool before comparing anything

- **The first attempt produced biologically impossible numbers** (07-28): heart rate jumping
  from 53 to 125 to 133 and down to 18.5 within a few seconds — while the participant was
  **lying still**.
  → **What this means:** rather than adjusting things until the numbers looked nicer, the
  decision was to stop. The cause was not in the filtering algorithm but in the
  **heart-rate measuring step** that comes before it. Three algorithms cannot be compared
  using a measurement that cannot be trusted.

- **Rebuilding the beat detection over three rounds** (07-28), each fixing a weakness of the
  previous one. After the rebuild, the LMS algorithm clearly won on the first participant.
  → **What this means:** like adjusting a ruler until it is accurate enough to measure with.
  *(Note added later: the third round of that rebuild — adding a constraint that heart rate
  may not jump too far between readings — turned out to be the thing that hid the project's
  largest error. See Week 13.)*

## Group 2 — Scaling to five people, and the result changing

- **A good result on one person did not survive scaling up** (07-28). Across five people:
  three improved, two got worse.
  → **What this means:** exactly why several people must be tested before drawing a
  conclusion. Reporting only the first participant's result would have published a
  conclusion that was true by chance in a single case.

- **Adding a second algorithm, and catching a serious numerical fault** (07-28). The RLS
  algorithm initially produced results off by hundreds of thousands of times, precisely
  during the periods when the participant was **standing, sitting or lying still**.
  → **What this means:** this kind of fault cannot be found by running the code and looking
  at the output — it takes understanding how the algorithm works inside to see that with
  almost no movement, one internal quantity grows without bound. Fixed by resetting that
  quantity above a threshold.

- **Adding a third algorithm and completing the four-way comparison** (07-28).

| Processing | Average error *(this number was later overturned)* |
| :--- | ---: |
| No filtering | 26.95 |
| NLMS | 26.96 |
| RLS | 29.83 |
| Wiener | 29.96 |

→ **What this means:** no algorithm proved consistently better than **doing nothing at
all**. This is a genuine research result: science does not always find the best method —
proving that "this approach is not good enough, a different one is needed" is also a
contribution, as long as the measurement is done seriously.

## Group 3 — Two final experiments, and a decision to stop

- **Trying three separate sensor axes instead of one combined value** (07-28): **worse for
  every algorithm**. Reason: too many parameters to estimate for the amount of data
  available. The combined approach was kept.

- **Investigating why one participant made two algorithms fail badly** (07-28): that person
  had the highest correlation between heart signal and movement, suggesting the algorithm
  was eating the real signal along with the noise when the two look too alike. But another
  person with almost the same correlation was **not** affected — so **the evidence was not
  sufficient** and the investigation stopped there.
  → **What this means:** deliberately stopping rather than digging indefinitely without new
  clues. Recorded clearly as an unconfirmed hypothesis, not a conclusion.

---

## Where things stood at the end of the week

The three-algorithm comparison was complete, with "no filtering" as the control. The
conclusion at the time: no algorithm demonstrated a consistent benefit.

**That conclusion was overturned in Week 13** — not because the algorithms are better than
we thought, but because the ruler used to mark them was broken.

## How this differed from the original plan

The original plan said *"Web BLE dashboard and final enclosure"*. In practice the whole
week went into the research track, built from scratch to result in a single working session.

**Which thesis chapter this feeds:** Chapter 4 sections 4.1–4.2 (experiment design and
first-round results). This week's conclusion is overturned in sections 4.3–4.6.

---
[← Week 9](week_09.md) · [Weekly reports index](README.md) · [Week 11 →](week_11.md)
