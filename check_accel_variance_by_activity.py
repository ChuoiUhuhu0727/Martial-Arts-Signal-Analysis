"""
Case (b) risk check for the LMS/RLS/Wiener track: is the accel signal too flat
during static postures (lying/sitting/standing) to be a useful noise reference
for adaptive filtering, compared to dynamic activities (walking/running)?

Uses std_mag from data/processed/master_dataset.csv -- the windowed std of accel
magnitude already computed on-device -- as a fast proxy for reference-signal
energy. Not a substitute for inspecting the actual raw waveform the filter would
use, but cheap enough to answer "is there a real problem here" before designing
anything (see CHANGELOG.md for the related 2026-07-22 no-motion-session rule,
same underlying metric).

Usage:
    python check_accel_variance_by_activity.py
"""
import pandas as pd

IN_PATH = "data/processed/master_dataset.csv"
ACTS = ["lying", "sitting", "standing", "walking", "running"]
STATIC = {"lying", "sitting", "standing"}


def main():
    df = pd.read_csv(IN_PATH)
    df = df[df["is_transition"] == 0].copy()

    print(f"Clean rows: {len(df)} | participants: {df['participant_id'].nunique()}")

    print("\n=== std_mag by activity (pooled across all participants) ===")
    summary = df.groupby("label")["std_mag"].agg(["median", "mean", "std", "count"]).reindex(ACTS)
    print(summary.to_string(float_format=lambda x: f"{x:.3f}"))

    static_median = df[df["label"].isin(STATIC)]["std_mag"].median()
    dynamic_median = df[~df["label"].isin(STATIC)]["std_mag"].median()
    print(f"\nstatic median std_mag:  {static_median:.3f}")
    print(f"dynamic median std_mag: {dynamic_median:.3f}")
    print(f"ratio dynamic/static:   {dynamic_median / static_median:.2f}x")

    # Pooled averages can hide a participant where static isn't actually flat --
    # an LMS filter runs per-session, not pooled across the dataset, so this is
    # the number that actually matters for case (b).
    print("\n=== per-participant median std_mag: static vs dynamic ===")
    rows = []
    for pid, g in df.groupby("participant_id"):
        s = g[g["label"].isin(STATIC)]["std_mag"].median()
        d = g[~g["label"].isin(STATIC)]["std_mag"].median()
        rows.append((pid, s, d, d / s if s > 0 else float("inf")))
    per_p = pd.DataFrame(rows, columns=["participant_id", "static_median", "dynamic_median", "ratio"])
    print(per_p.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n=== static activities broken out (lying/sitting/standing aren't necessarily equally flat) ===")
    for act in ["lying", "sitting", "standing"]:
        vals = df[df["label"] == act]["std_mag"]
        print(f"  {act:>8s}: median={vals.median():.3f}  mean={vals.mean():.3f}  n={len(vals)}")


if __name__ == "__main__":
    main()
