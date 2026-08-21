# Week 11 Report — Putting the AI on the real device and testing it on a wrist

## What this week was about — the overview

**Phase:** Phase 3 — *Polish and Documentation* (Weeks 10–13). Matches milestone **M6**:
full system integration.

**In one sentence:** for the first time, **wearing the actual device** and watching the AI
recognise activities live, after many weeks of running only on a laptop.

**Why it matters:** a model that works well on a laptop does not automatically work
correctly on the small chip inside the device. This week answers: **do the laptop results
survive the move to real hardware?**

---

## Group 1 — Moving the model from laptop to chip

![Figure 11.1: The three steps for getting the AI onto the device. The second step was complete, but nobody had connected it to the program actually running on the device.](figures_en/week11_train_to_device.png)

- **Writing a tool that translates the model into code the chip can read** (07-28).
  → **What this means:** the model is trained in Python on a laptop, but the chip in the
  wrist device is not powerful enough to run Python. The trained model has to be
  "translated" into code that runs directly on the chip. This step is what makes the trained
  AI actually work on the device rather than stopping at the laptop.

- **Discovering the translation was done but never wired in** (07-28). Only after loading it
  onto the device did it become clear the program was still calling the **old** model.
  → **What this means:** a very common fault in systems with several parts — each part is
  correct on its own, but the step of connecting them was forgotten. Without loading it onto
  the real device, this fault would never have surfaced.

- **Removing an old rule that would have broken the new model** (07-28). The old program had
  a rule: *when the device is nearly still, assume "lying"*. That was right for the old model
  (which only told hard exercise from light), but **completely wrong** for the new one.
  → **What this means:** being still is exactly when the new model is needed most — that is
  when it has to tell lying from sitting from standing. The old rule would have disabled the
  new model's main function. Removed just in time, before it silently corrupted results.

## Group 2 — Testing on a real person

- **Loaded onto the device, worn on a wrist, one test session recorded** (07-29). Result:
  **running correct 99%, standing correct 76%** live — even better than on the laptop. Lying
  and sitting were still confused with standing.
  → **What this means:** the pattern of confusion **matched exactly** what was predicted at
  training time. That confirms two things: the translation onto the device was done
  correctly, and no new fault appeared in moving from laptop to hardware.

- **An odd result investigated, and traced to operator error rather than AI error** (07-29).
  A "walking" segment was classified as "standing" 95% of the time. Checking the data: the
  measured shaking was about **one tenth** of real walking.
  → **What this means:** the tester was actually **standing still adjusting the device**
  while the machine was labelling it "walking". So the fault was in carrying out the
  experiment, not in the AI. That session was removed from the main dataset. This is the
  right reflex: when a number looks strange, investigate before concluding "the AI is broken".

## Group 3 — Recording a process gap, and deciding not to fix it yet

- **The automatic sorting program cannot tell real data from test data** (07-29). Cleaned up
  by hand this time, to be fixed if it recurs.
  → **What this means:** a conscious prioritisation decision — not fixing everything the
  moment it is found, if it is not yet clear the problem will recur. But written down
  clearly so it is not forgotten.

---

## Where things stood at the end of the week

The five-class model **runs on real hardware**, and the live results match the laptop
results. This confirms the whole chain *train → translate → load onto device* works
correctly, with no drift introduced by integration.

## How this differed from the original plan

The original plan said *"Stability testing and full validation"*. There was no 60-minute
continuous run — this week's validation was a single short session, not an endurance test.

**Which thesis chapter this feeds:** Chapter 2 section 2.1 (firmware architecture) and
Chapter 5 section 5.1 (how the two subsystems fit together).

---
[← Week 10](week_10.md) · [Weekly reports index](README.md) · [Week 12 →](week_12.md)
