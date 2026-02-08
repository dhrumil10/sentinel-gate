import os
import sys
import copy
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sentinelgate import load_config, SentinelGate


def eval_with_tau(df: pd.DataFrame, tau: float):
    cfg = load_config()

    # ✅ keep Thresholds as a Thresholds object (not a dict)
    new_thresholds = cfg.thresholds.model_copy(update={"layer2_margin_tau": tau})
    cfg = cfg.model_copy(update={"thresholds": new_thresholds})




    gate = SentinelGate(cfg)

    y_true, y_pred = [], []
    cats = []

    for _, row in df.iterrows():
        prompt = str(row["prompt"])
        expected = str(row["label"]).strip().lower()
        category = str(row.get("category", "unknown"))

        d = gate.check(prompt)
        pred = "allow" if d.decision == "ALLOW" else "block"

        y_true.append(expected)
        y_pred.append(pred)
        cats.append(category)

    # metrics
    total = len(y_true)
    acc = sum(t == p for t, p in zip(y_true, y_pred)) / max(1, total)

    # allow recall = TP_allow / (TP_allow + FN_allow)
    tp_allow = sum(1 for t, p in zip(y_true, y_pred) if t == "allow" and p == "allow")
    fn_allow = sum(1 for t, p in zip(y_true, y_pred) if t == "allow" and p == "block")
    allow_recall = tp_allow / max(1, (tp_allow + fn_allow))

    # block precision = TP_block / (TP_block + FP_block)
    tp_block = sum(1 for t, p in zip(y_true, y_pred) if t == "block" and p == "block")
    fp_block = sum(1 for t, p in zip(y_true, y_pred) if t == "allow" and p == "block")
    block_precision = tp_block / max(1, (tp_block + fp_block))

    # category accuracies
    out = pd.DataFrame({"category": cats, "correct": [t == p for t, p in zip(y_true, y_pred)]})
    by_cat = (out.groupby("category")["correct"].mean() * 100).to_dict()

    return {
        "tau": tau,
        "accuracy_pct": acc * 100,
        "allow_recall": allow_recall,
        "block_precision": block_precision,
        "domain_acc_pct": by_cat.get("domain_specific", None),
        "generic_acc_pct": by_cat.get("generic_work", None),
        "junk_acc_pct": by_cat.get("junk", None),
        "false_negatives_allow": fn_allow,
        "false_positives_allow": 0,  # same as FP_block
        "false_positives_block": fp_block,
    }


def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sentinelgate_research_data.csv")
    df = pd.read_csv(data_path)

    taus = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
    rows = [eval_with_tau(df, t) for t in taus]

    res = pd.DataFrame(rows)
    print("\n=== Tau Sweep (layer2_margin_tau) ===")
    print(res[[
        "tau",
        "accuracy_pct",
        "allow_recall",
        "block_precision",
        "domain_acc_pct",
        "generic_acc_pct",
        "junk_acc_pct",
        "false_negatives_allow",
        "false_positives_block",
    ]].to_string(index=False))

    out_path = os.path.join(os.path.dirname(__file__), "tau_sweep_results.csv")
    res.to_csv(out_path, index=False)
    print("\nSaved:", out_path)


if __name__ == "__main__":
    main()
