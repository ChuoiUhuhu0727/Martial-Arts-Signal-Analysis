"""
Train the 5-class activity classifier (lying/sitting/standing/walking/running) on
data/processed/master_dataset.csv (N=17 participants) and export it.

Uses DecisionTreeClassifier(max_depth=5, min_samples_leaf=5) -- same model/hyperparams
already validated in logo_cv_activity_features.py, kept consistent rather than
introducing a new model choice at export time.

bug-1 (see CHANGELOG.md / project memory 2026-07-28) is a CLOSED rabbit hole: magnitude
-based features can't carry orientation info, so lying/sitting/standing confusion in the
LOGO-CV report below is an expected, root-caused finding -- report it honestly, it is not
a blocker and not something to re-investigate here.

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
ACTS = ["lying", "sitting", "standing", "walking", "running"]


def make_model():
    return DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, random_state=0)


def main():
    df = pd.read_csv(IN_PATH)
    df = df[df["is_transition"] == 0].copy()

    X = df[FEATURES].values
    y = df["label"].values
    groups = df["participant_id"].values
    logo = LeaveOneGroupOut()

    print(f"Clean rows: {len(df)} | participants: {df['participant_id'].nunique()}")
    print(f"Features: {FEATURES}")

    fold_acc = []
    all_true, all_pred = [], []
    for train_idx, test_idx in logo.split(X, y, groups):
        clf = make_model()
        clf.fit(X[train_idx], y[train_idx])
        pred = clf.predict(X[test_idx])
        held_out = groups[test_idx][0]
        acc = accuracy_score(y[test_idx], pred)
        fold_acc.append((held_out, acc))
        all_true.extend(y[test_idx])
        all_pred.extend(pred)

    print(f"\n=== LOGO-CV: 5-class (features: {FEATURES}) ===")
    for pid, acc in sorted(fold_acc):
        print(f"  held-out {pid}: accuracy = {acc:.3f}")
    mean_acc = np.mean([a for _, a in fold_acc])
    print(f"  mean across {len(fold_acc)} folds: {mean_acc:.3f}")

    cm = confusion_matrix(all_true, all_pred, labels=ACTS)
    print("\n  pooled confusion matrix (rows=true, cols=pred):")
    print("  " + " ".join(f"{a[:4]:>6s}" for a in ACTS))
    for i, a in enumerate(ACTS):
        print(f"  {a[:4]:>4s} " + " ".join(f"{cm[i][j]:6d}" for j in range(len(ACTS))))

    # Per-class recall -- makes the lying/sitting/standing confusion (bug-1, closed
    # rabbit hole) visible directly instead of being hidden by overall accuracy.
    print("\n  per-class recall:")
    for i, a in enumerate(ACTS):
        recall = cm[i][i] / cm[i].sum() if cm[i].sum() > 0 else float("nan")
        print(f"    {a:>8s}: {recall:.3f}")

    # Final export model: trained on ALL 17 participants (LOGO-CV above is for
    # honest accuracy reporting only, not the deployed model).
    final_model = make_model()
    final_model.fit(X, y)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    joblib.dump({"model": final_model, "features": FEATURES, "classes": list(final_model.classes_)}, OUT_PATH)
    print(f"\nFinal model (trained on all {df['participant_id'].nunique()} participants) saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
