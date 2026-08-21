# Week 6 Report — Hardening the data collection pipeline

## What this week was about — the overview

**Phase:** Phase 2 — *Edge AI Integration* (Weeks 5–9), still on step 1 of the project:
collecting data.

**In one sentence:** Week 5 got the collection process working. This week went one level
deeper — fixing the faults that made the collected data **look correct while actually being
wrong**.

**Why it matters:** this is the most dangerous class of fault in the whole project. A
session that breaks partway is obvious to everyone. But a session that runs to the end,
records the right number of rows, and has labels that are wrong for the first few seconds —
nobody notices, and the AI learns exactly that wrongness.

---

## Group 1 — Making the labels match reality

![Figure 6.1: One session is 15 seconds of preparation plus five activities of 90 seconds each. Before the fix, recording began the moment the device powered on, labelling data as "lying" while the participant was still standing up.](figures_en/week06_protocol_timeline.png)

- **Adding 15 seconds of preparation before the first activity, and moving the prompt sound
  to the laptop** (07-14).
  → **What this means:** before this, the device began recording the instant it powered on.
  The participant had not lain down yet, but the machine already counted it as "lying" —
  the label was wrong from the very first second. The prompt sound that tells the
  participant to change position moved to the laptop, because the small speaker on the
  device misbehaved on battery power. This directly improves **label accuracy**, which is
  the foundation for the AI learning the right thing.

- **Checking sensor skin contact continuously instead of once at power-on** (07-14).
  → **What this means:** the heart rate sensor has to sit against the skin to read
  correctly. Previously the system checked exactly once at startup and then assumed it
  stayed true for the whole session — even though a participant could shift the sensor
  midway without anyone knowing. Now it re-checks periodically and records the result in
  both the stored data and the live view.

## Group 2 — Measuring heart rate more reliably

- **A beat-detection threshold that adapts to each person** (07-15).
  → **What this means:** the system recognises each heartbeat by tracking changes in the
  light reflected off the skin. The old detection threshold was a fixed number, which did
  not suit the different signal strengths of different people — so the machine sometimes
  "saw no beats at all" for tens of seconds while the heart was beating normally. The fix
  makes the threshold stretch to match the actual signal. A new data column marks the
  moments when a beat was genuinely just detected, so that later we can tell "the machine
  just measured this" apart from "the machine is repeating an old number".

## Group 3 — Laying the groundwork for the research track

- **Retrieving data no longer requires pressing a button on the device** (07-14).
  → **What this means:** previously a physical button had to be pressed to extract data
  after each session — but once the device was fitted into its enclosure, that button was
  covered. Fixed so the command can be issued from the laptop instead.

- **Starting to record a raw signal stream alongside the main data** (07-15).
  → **What this means:** besides the two main goals (activity recognition and heart rate),
  the project has a separate research question: comparing three methods for removing noise
  caused by arm movement. A fair comparison has to run the algorithms on the **raw,
  unprocessed signal**, not on an already-computed heart rate number. This week that raw
  stream started being recorded, laying the groundwork for Week 10.

---

## Where things stood at the end of the week

| Before this week | After this week |
| :--- | :--- |
| Labels wrong for the first seconds of each activity | 15 seconds of preparation; labels match reality |
| Skin contact checked only once | Checked continuously through the session |
| Heart rate frozen for tens of seconds | Threshold adapts to each person |
| Only the computed heart rate stored | Raw signal stored as well, for research |

## How this differed from the original plan

The original plan said *"Model training, quantization, and PCB order"*. In practice there
was not yet enough data to train a model — this week continued strengthening the collection
side first. The PCB order is outside the scope of this repository.

**Which thesis chapter this feeds:** Chapter 2, sections 2.1 and 2.2 (device architecture
and collection protocol).

---
[← Week 5](week_05.md) · [Weekly reports index](README.md) · [Week 7 →](week_07.md)
