"""
Train the 5-class activity classifier (lying/sitting/standing/walking/running) on
data/processed/master_dataset.csv and export it. Also reports the 3-class
(stationary/walking/running, via the activity_group column) LOGO-CV accuracy for
comparison -- see CHANGELOG.md 2026-07-30 for why this second number matters: it's
the same model/features/data, just regrouped to match what the feature set can
actually support, and it's the "solution C" step of the classifier finding's story
(finding: 54.7% 5-class -> root cause: magnitude can't carry orientation info ->
regroup to 3-class -> 85.3%). Previously this comparison was run ad hoc in a chat
session with no saved script -- folded into this file so it's reproducible from a
single command instead of unable to be shown to anyone.

Uses DecisionTreeClassifier(max_depth=5, min_samples_leaf=5) -- same model/hyperparams
already validated in logo_cv_activity_features.py, kept consistent rather than
introducing a new model choice at export time.

bug-1 (see CHANGELOG.md / project memory 2026-07-28) is a CLOSED rabbit hole: magnitude
-based features can't carry orientation info, so lying/sitting/standing confusion in the
5-class LOGO-CV report below is an expected, root-caused finding -- report it honestly,
it is not a blocker and not something to re-investigate here.

Usage:
    python train_activity_classifier.py
"""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import os

IN_PATH = "data/processed/master_dataset.csv"
OUT_PATH = "models/activity_classifier.pkl"
FEATURES = ["mean_mag", "std_mag", "peak_rel", "peak_max"]
ACTS_5CLASS = ["lying", "sitting", "standing", "walking", "running"]
ACTS_3CLASS = ["stationary", "walking", "running"]


def make_model():
    return DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, random_state=0)


def run_logocv(X, y, groups, class_labels, title):
    """Shared LOGO-CV runner -- same model/procedure regardless of which column
    (label vs activity_group) is used as the target, so the two accuracy numbers
    are a fair apples-to-apples comparison, not different methodologies."""
    logo = LeaveOneGroupOut()
    fold_acc = []
    all_true, all_pred = [], []
    for train_idx, test_idx in logo.split(X, y, groups):
        clf = make_model()
        clf.fit(X[train_idx], y[train_idx])
        pred = clf.predict(X[test_idx])
        held_out = groups[test_idx][0]
        fold_acc.append((held_out, accuracy_score(y[test_idx], pred)))
        all_true.extend(y[test_idx])
        all_pred.extend(pred)

    print(f"\n=== LOGO-CV: {title} ===")
    for pid, acc in sorted(fold_acc):
        print(f"  held-out {pid}: accuracy = {acc:.3f}")
    mean_acc = np.mean([a for _, a in fold_acc])
    print(f"  mean across {len(fold_acc)} folds: {mean_acc:.3f}")

    cm = confusion_matrix(all_true, all_pred, labels=class_labels)
    print("\n  pooled confusion matrix (rows=true, cols=pred):")
    print("  " + " ".join(f"{a[:4]:>6s}" for a in class_labels))
    for i, a in enumerate(class_labels):
        print(f"  {a[:4]:>4s} " + " ".join(f"{cm[i][j]:6d}" for j in range(len(class_labels))))

    print("\n  per-class recall:")
    for i, a in enumerate(class_labels):
        recall = cm[i][i] / cm[i].sum() if cm[i].sum() > 0 else float("nan")
        print(f"    {a:>10s}: {recall:.3f}")

    return mean_acc


def main():
    df = pd.read_csv(IN_PATH)
    df = df[df["is_transition"] == 0].copy()

    X = df[FEATURES].values
    groups = df["participant_id"].values

    print(f"Clean rows: {len(df)} | participants: {df['participant_id'].nunique()}")
    print(f"Features: {FEATURES}")

    acc_5class = run_logocv(X, df["label"].values, groups, ACTS_5CLASS,
                             "5-class (lying/sitting/standing/walking/running)")
    acc_3class = run_logocv(X, df["activity_group"].values, groups, ACTS_3CLASS,
                             "3-class (stationary/walking/running, same features/model/data)")

    print(f"\n=== Summary: same model+features+data, two scopes ===")
    print(f"  5-class mean accuracy: {acc_5class:.3f}")
    print(f"  3-class mean accuracy: {acc_3class:.3f}")

    # Final export model: 5-class, trained on ALL participants (LOGO-CV above is for
    # honest accuracy reporting only, not the deployed model). 5-class is what's
    # deployed to firmware_ble (see activity_classifier_5class.h) -- the 3-class
    # number above is reported for context/comparison, not a second deployed model.
    y = df["label"].values
    final_model = make_model()
    final_model.fit(X, y)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    joblib.dump({"model": final_model, "features": FEATURES, "classes": list(final_model.classes_)}, OUT_PATH)
    print(f"\nFinal model (trained on all {df['participant_id'].nunique()} participants) saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
