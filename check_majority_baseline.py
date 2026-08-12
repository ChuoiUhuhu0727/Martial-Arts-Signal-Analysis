"""
Section 4 support (activity_classifier_report_OUTLINE.md): what would a trivial
majority-class baseline score on the 5-class vs 3-class problem, so the reported
LOGO-CV accuracy (0.548 / 0.853) can be judged against something, not just each
other?

Uses data/processed/master_dataset.csv directly (same file the classifier trains
on) -- no model involved, just class counts.

Usage:
    python check_majority_baseline.py
"""
import pandas as pd

IN_PATH = "data/processed/master_dataset.csv"


def main():
    df = pd.read_csv(IN_PATH)
    print(f"Total rows: {len(df)}")

    print("\n=== 5-class (label) distribution ===")
    vc = df["label"].value_counts()
    print(vc.to_string())
    print(f"Majority-class baseline (5-class): {vc.max() / len(df):.4f}")
    print(f"Random-guess baseline (5-class, 1/5): {1/5:.4f}")

    print("\n=== 3-class (activity_group) distribution ===")
    vc2 = df["activity_group"].value_counts()
    print(vc2.to_string())
    print(f"Majority-class baseline (3-class): {vc2.max() / len(df):.4f}")
    print(f"Random-guess baseline (3-class, 1/3): {1/3:.4f}")


if __name__ == "__main__":
    main()
