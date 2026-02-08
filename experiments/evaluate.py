import os
import sys
import time
import pandas as pd

# Make imports work when running as a script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sentinelgate import load_config, SentinelGate


def safe_div(a, b):
    return a / b if b else 0.0


def confusion_metrics(y_true, y_pred, labels):
    # labels: list like ["allow", "block"]
    idx = {l: i for i, l in enumerate(labels)}
    m = [[0 for _ in labels] for _ in labels]
    for t, p in zip(y_true, y_pred):
        if t in idx and p in idx:
            m[idx[t]][idx[p]] += 1

    # per label precision/recall/f1
    metrics = {}
    for l in labels:
        i = idx[l]
        tp = m[i][i]
        fp = sum(m[r][i] for r in range(len(labels)) if r != i)
        fn = sum(m[i][c] for c in range(len(labels)) if c != i)
        precision = safe_div(tp, tp + fp)
        recall = safe_div(tp, tp + fn)
        f1 = safe_div(2 * precision * recall, precision + recall)
        metrics[l] = {"precision": precision, "recall": recall, "f1": f1, "support": sum(m[i])}

    return m, metrics


def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sentinelgate_research_data.csv")
    if not os.path.exists(data_path):
        print("❌ Missing dataset:", data_path)
        return

    df = pd.read_csv(data_path)
    cfg = load_config()
    gate = SentinelGate(cfg)

    y_true, y_pred = [], []
    layers = []
    cats = []

    start = time.perf_counter()
    for _, row in df.iterrows():
        prompt = str(row["prompt"])
        expected = str(row["label"]).strip().lower()
        category = str(row.get("category", "unknown"))

        d = gate.check(prompt)

        pred = "allow" if d.decision == "ALLOW" else "block"
        y_true.append(expected)
        y_pred.append(pred)
        cats.append(category)

        if d.reason.startswith("junk_"):
            layers.append("L0")
        elif d.reason == "semantic_noise":
            layers.append("L1")
        else:
            layers.append("L2")

    dur = time.perf_counter() - start

    acc = sum(t == p for t, p in zip(y_true, y_pred)) / max(1, len(y_true))
    print("\n=== SentinelGate Evaluation ===")
    print(f"Samples: {len(y_true)}")
    print(f"Accuracy: {acc*100:.2f}%")
    print(f"Total eval time: {dur:.2f}s  |  Avg per prompt: {(dur/max(1,len(y_true)))*1000:.2f}ms")

    labels = ["allow", "block"]
    cm, per = confusion_metrics(y_true, y_pred, labels)

    print("\nConfusion Matrix (rows=true, cols=pred)  [allow, block]")
    print(cm)

    print("\nPer-class metrics")
    for l in labels:
        print(
            f"{l:>5} | P={per[l]['precision']:.3f}  R={per[l]['recall']:.3f}  "
            f"F1={per[l]['f1']:.3f}  support={per[l]['support']}"
        )

    # Breakdown by category
    out = pd.DataFrame({"category": cats, "correct": [t == p for t, p in zip(y_true, y_pred)]})
    print("\nBreakdown by category (accuracy %)")
    print((out.groupby("category")["correct"].mean() * 100).round(2))

    # Breakdown by layer caught
    out2 = pd.DataFrame({"layer": layers})
    print("\nBlocking layer counts")
    print(out2["layer"].value_counts())


if __name__ == "__main__":
    main()
