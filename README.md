# SentinelGate: Cost-Efficient LLM Guardrails 🛡️

**A Hierarchical "Cheap-First" Architecture for Enterprise AI Governance.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Accuracy](https://img.shields.io/badge/accuracy-92.44%25-green)
![Latency](https://img.shields.io/badge/avg_latency-9.65ms-brightgreen)

## 📌 Abstract
SentinelGate is a lightweight, pre-flight guardrail system designed to reduce Enterprise LLM costs by **40%+**. It blocks irrelevant and off-domain prompts *before* they hit expensive LLM APIs.

Unlike standard guardrails that focus on safety (hate speech), SentinelGate focuses on **FinOps and Domain Relevance**. It uses a 3-stage hierarchical filtering pipeline to distinguish between **Valid Supply Chain Queries** and **Generic Corporate Noise** (like HR/IT tickets) with **92.44% accuracy** on a 119-prompt dataset.

## 🚀 The Architecture
The system uses a "Cascading Cost" design: cheap checks run first; expensive checks run last.

1. **Layer 0 (Regex/Heuristic):** Instantly blocks junk/spam (e.g., "hi", "test", symbols-only) in <1ms.
2. **Layer 1 (Semantic Noise):** Uses `sentence-transformers/all-MiniLM-L6-v2` to detect chitchat (e.g., "Tell me a joke") in ~10ms.
3. **Layer 2 (Contrastive Domain):** A margin-based "Positive vs. Negative Anchor" check that distinguishes Domain Work (Supply Chain) from Generic Work (HR/IT/Admin).

### 🔧 What is Tau?
Layer 2 uses a margin score:
- `margin = similarity(domain_positive) - similarity(domain_negative)`
- A prompt is **allowed** if `margin >= tau`

Lower tau (e.g., 0.05) is more permissive (higher recall), higher tau (e.g., 0.10) is stricter (lower risk of off-domain passing).
For enterprise usage, SentinelGate recommends **tau = 0.10**.

## ✅ Prompt Sanitization (New)
SentinelGate includes a safe prefix sanitizer that removes greeting/filler prefixes to reduce false blocks and improve domain matching.

Example:
- `hey, where is my shipment` → `where is my shipment`

The API returns both `original_prompt` and `clean_prompt` for transparency.

## 📊 Benchmark Results
Tested on a synthetic dataset of 119 enterprise prompts.

| Metric | Result |
| :--- | :--- |
| **Overall Accuracy** | **92.44%** |
| **Junk Blocking** | 100.0% |
| **Generic Blocking** | 100.0% |
| **Domain Accuracy** | 80.0% |
| **Avg Latency** | ~9.65 ms |
| **Est. Cost Savings** | ~$1.26 per 100 requests |

## 🛠️ Installation & Usage

### 1. Clone the Repo
```bash
git clone https://github.com/dhrumil10/sentinel-gate.git
cd sentinel-gate
```
### 2. Install Dependencies
```bash
python -m venv venv
```
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```bash
pip install -r requirements.txt
```

## 🚀 Run the API (FastAPI)

### From repo root:
```bash
Windows PowerShell
$env:PYTHONPATH="."
uvicorn src.main:app --reload
```

### Mac/Linux
```bash
export PYTHONPATH="."
uvicorn src.main:app --reload
```

### Open Swagger:
```
http://127.0.0.1:8000/docs
```

## 🔌 API Endpoints
```
GET / → health check

POST /scan → scan a prompt (PASS/BLOCK)

GET /analytics → FinOps metrics (blocked count, estimated savings)

Example /scan Response
{
  "decision": "PASSED",
  "layer_caught": "L2",
  "reason": "domain_match",
  "gate_latency_ms": 40.08,
  "action": "SEND_TO_LLM",
  "original_prompt": "hey, where is my shipment",
  "clean_prompt": "where is my shipment",
  "debug": { "similarity": 0.48, "margin": 0.31 }
}
```

## 🧪 Experiments
### 1) Evaluate (metrics + confusion matrix)
# Windows PowerShell
```
$env:PYTHONPATH="."
python experiments/evaluate.py
```

### 2) Tune Tau (sweep margin threshold)
# Windows PowerShell
```
$env:PYTHONPATH="."
python experiments/tune_tau.py
```

### Outputs:
```
prints tau sweep table

saves: experiments/tau_sweep_results.csv
```

## ⚙️ Configuration

### SentinelGate is config-driven via config.yaml:

### domain name

**Layer 0 rules**

**Layer 1 anchors**

**Layer 2 positive/negative anchors**

thresholds (layer1_noise_max_sim, layer2_margin_tau)

**Important**:

keep layer2_margin_tau only once in config.yaml

### Recommended enterprise config:

**layer2_margin_tau**: 0.10

## 📄 Research & Citation

This project supports a research direction around FinOps-driven LLM governance and domain relevance filtering.

### Proposed paper title:
"SentinelGate: A Hierarchical Cheap-First Guardrail Architecture for Cost-Efficient Domain Relevance"

::contentReference[oaicite:0]{index=0}
