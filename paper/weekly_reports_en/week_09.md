# Week 9 Report — First model trained, and the root cause found

## What this week was about — the overview

**Phase:** Phase 2 — *Edge AI Integration*, the last week of that phase. The project moved
to **step 3: training the AI model**. Matches milestone **M3** in the plan.

**In one sentence:** trained the first model (54.8% accuracy), and more importantly —
**found the mathematical reason** why it cannot do better with the current sensor.

**Why it matters:** this was the turning point. Before this week, the AI confusing the
three still postures was a *bug to be fixed*. After this week it became an *explained
result* — and that changed the direction of the rest of the project entirely.

---

## Group 1 — Automating the whole path the data travels

- **A program that sorts and files data automatically after each session** (07-28). It
  applies the fake-session rule from Week 8, moves files to the right folders, and adds a
  row to the participant log.
- **A program that builds the training dataset from the original data** (07-28), including
  a ready-made grouping column so that both the five-class and three-class versions can be
  trained later without re-running anything.
  → **What this means:** from this week on, the path *collect → process → train* runs end
  to end **with no manual step anywhere**. This is what makes every number in later reports
  reproducible.

- **Two more participants added**, bringing the dataset to 17 people.

## Group 2 — Marking the AI fairly

![Figure 9.1: In each round of marking, one person is held out as the test, and the AI may only learn from the other 17. Repeated for all 18 rounds.](figures_en/week09_logocv.png)

The model is marked by **holding out one person at a time as the test**: the AI learns from
17 people, then is tested on the 18th, whom it has never seen. This repeats until everyone
has been the test once, and the results are averaged.

→ **What this means:** if one person's data went into both the learning and the testing
set, the AI could score highly just by recognising that person — a very pretty number that
means nothing, because in real life the AI always meets new people. This marking scheme
gives the **real** number for a stranger.

## Group 3 — The result, and why one average is not enough

**Result: 54.8% average accuracy.** But that number hides what is actually happening:

| Activity | Correctly identified | |
| :--- | ---: | :--- |
| Lying | 28.4% | barely above random guessing (20%) |
| Sitting | 46.9% | |
| Standing | 55.1% | |
| Walking | 64.6% | good |
| Running | 78.2% | very good |

→ **What this means:** the model is **not uniformly mediocre**. It is very good at the two
moving activities and almost blind at one still posture. Reporting only 54.8% would leave a
reader thinking "an average model that needs more tuning" — when in fact there is one very
specific thing broken.

### Why the three still postures cannot be separated

All four features fed to the model are computed from the **magnitude** of acceleration,
that is `√(ax² + ay² + az²)` — the **length** of the acceleration arrow in space.

When the wearer rotates their wrist, that arrow changes **direction** but **not length**.
And lying, sitting and standing differ precisely in wrist **direction**, while barely
differing in how much movement there is.

→ **Conclusion:** the information needed to tell those three apart is **erased at the
feature extraction step**, before the model ever sees the data. This is a **structural**
limit, not a bad parameter choice. No amount of model tuning can recover it.

Walking and running, by contrast, differ clearly in **amount of movement** — exactly what
magnitude does measure — so those two separate very well.

## Group 4 — Deciding to stop at the right moment

- **Closing the per-axis line of attack** (07-28). After a third variant tried on six
  people, the results got **more tangled rather than clearer**: the new fix dropped one
  person from 62.2% to 35.0%.
  → **What this means:** the decision was to stop trying more variants and report the
  problem honestly as an explained result, rather than keep patching. The real fix — adding
  a gyroscope and a calibration step — was written down for a future collection round, since
  it cannot be applied retroactively to data already gathered.

- **Evaluating the supervisor's suggestion of an AI model** (07-28): a good idea, but it
  needs considerably more participants than this project has. The classical-algorithm
  approach was kept, with the AI model noted as a possible later comparison.

---

## Where things stood at the end of the week

The path collect → process → train runs without manual intervention. The first five-class
model reaches **54.8%**. The three-still-postures problem officially changed from an
"outstanding bug" into **"a result whose cause is understood"**.

## How this differed from the original plan

The original plan said *"Integration debugging and stress testing"*. There was no long
endurance test on integrated hardware — validation on the real device happened in Week 11.

**Which thesis chapter this feeds:** Chapter 3 sections 3.2–3.4 (five-class result and root
cause), and Chapter 2 section 2.4 (the marking scheme).

---
[← Week 8](week_08.md) · [Weekly reports index](README.md) · [Week 10 →](week_10.md)
