"\

# SentinelGate: Cost-Efficient LLM Guardrails 🛡️\n\

\n
A hierarchical **cheap-first** guardrail for Enterprise LLM governance.\n
\n
![License](https://img.shields.io/badge/license-MIT-blue.svg)\n
![Python](https://img.shields.io/badge/python-3.9%2B-blue)\n
![Accuracy](https://img.shields.io/badge/accuracy-92.44%25-green)\n
![Latency](https://img.shields.io/badge/avg_latency-9.65ms-brightgreen)\n
\n\

## Abstract\n\

SentinelGate is a lightweight, pre-flight guardrail system built to reduce Enterprise LLM costs by blocking **irrelevant / off-domain / low-value prompts before they hit expensive LLM APIs**.\n
\n
Unlike standard guardrails that focus primarily on safety (hate speech, self-harm), SentinelGate focuses on:\n\

* **FinOps / cost efficiency** (stop wasteful calls)\n\
* **Domain relevance** (only allow prompts that match the organization’s domain)\n
  \n
  It uses a **3-layer hierarchical pipeline** to classify prompts as:\n\
* **ALLOW (send to LLM)**\n\
* **BLOCK (reject request)**\n
  \n\

## Key Idea\n\

Run the **cheapest checks first**, and only run more expensive semantic checks if needed.\n
\n\

## Architecture\n\

SentinelGate uses a cascading-cost design:\n
\n\

### Layer 0: Regex + Heuristics (ultra-cheap)\n\

Blocks obvious junk instantly:\n\

* single-word greetings (hi/hello)\n\
* test spam (test/ok)\n\
* symbol-only prompts\n
  \n\

### Layer 1: Semantic Noise Filter (cheap embeddings)\n\

Uses `sentence-transformers/all-MiniLM-L6-v2` to detect chitchat and generic noise:\n\

* “tell me a joke”\n\
* “how are you”\n
  \n\

### Layer 2: Contrastive Domain Check (positive vs negative anchors)\n\

Uses a **margin-based** contrastive decision:\n\

* Compare similarity to **domain-positive anchors** (Supply Chain)\n\
* Compare similarity to **domain-negative anchors** (HR/IT/Admin)\n\
* Decision is based on `margin = sim_pos - sim_neg` and a threshold `tau`\n
  \n\

## Results (Current)\n\

Dataset: synthetic enterprise prompt set (119 prompts)\n
\n
| Metric | Value |\n
| --- | --- |\n
| Overall Accuracy | 92.44% |\n
| Junk Accuracy (L0) | 100% |\n
| Generic Work Accuracy | 100% |\n
| Domain Specific Accuracy | 80% |\n
| Avg Latency / prompt | ~9.65 ms |\n
\n\

## Repository\n\

GitHub: [https://github.com/dhrumil10/sentinel-gate\n\](https://github.com/dhrumil10/sentinel-gate\n\)
\n\

## Project Layout\n\

* `src/main.py` → FastAPI API server (`/scan`, `/analytics`)\n\
* `src/sentinelgate/` → core pipeline (config + similarity + decision)\n\
* `src/sentinelgate/sanitize.py` → prefix sanitizer (removes “hey”, “please”, etc.)\n\
* `config.yaml` → config-driven anchors + thresholds\n\
* `data/sentinelgate_research_data.csv` → evaluation dataset\n\
* `experiments/evaluate.py` → metrics + confusion matrix\n\
* `experiments/tune_tau.py` → tau sweep + CSV output\n
  \n\

## Installation\n\

\n\

1. Clone\n\

* git clone [https://github.com/dhrumil10/sentinel-gate.git\n\](https://github.com/dhrumil10/sentinel-gate.git\n\)
* cd sentinel-gate\n
  \n\

2. Create venv\n
   Windows PowerShell:\n\

* python -m venv venv\n\
* .\venv\Scripts\Activate.ps1\n
  \n
  Mac/Linux:\n\
* python -m venv venv\n\
* source venv/bin/activate\n
  \n\

3. Install dependencies\n\

* pip install -r requirements.txt\n
  \n\

## Configuration\n\

SentinelGate is **config-driven**. Update `config.yaml` to change:\n\

* domain name\n\
* L0 junk rules\n\
* L1 noise anchors\n\
* L2 positive/negative anchors\n\
* thresholds (including tau)\n
  \n
  Important: `layer2_margin_tau` should appear only once.\n
  Recommended (enterprise-friendly) example:\n\
* thresholds:\n\

  * layer1_noise_max_sim: 0.5\n\
  * layer2_margin_tau: 0.10\n
    \n\

## Run the API\n\

From repo root:\n
\n
Option A (recommended):\n\

* set PYTHONPATH=. (so imports work)\n\
* run uvicorn src.main:app\n
  \n
  Windows PowerShell:\n\
* $env:PYTHONPATH = "."\n\
* uvicorn src.main:app --reload\n
  \n
  Mac/Linux:\n\
* export PYTHONPATH=.\n\
* uvicorn src.main:app --reload\n
  \n
  Then open:\n\
* Swagger UI: [http://127.0.0.1:8000/docs\n\](http://127.0.0.1:8000/docs\n\)
  \n\

## API Endpoints\n\

* GET `/` → health check\n\
* POST `/scan` → main guardrail decision\n\
* GET `/analytics` → real-time FinOps counters\n
  \n\

### Scan Response\n\

`/scan` returns:\n\

* decision: PASSED or BLOCKED\n\
* layer_caught: L0 / L1 / L2\n\
* reason\n\
* gate_latency_ms\n\
* original_prompt and clean_prompt\n\
* debug (similarity, margin)\n
  \n\

## Sanitization\n\

Before scanning, SentinelGate runs a safe prefix sanitizer:\n\

* removes greeting/filler prefixes only (e.g., “hey,” “please,” “quick question”)\n\
* does not remove content from the middle of the prompt\n
  \n
  Example:\n\
* "hey, where is my shipment" → "where is my shipment"\n
  \n\

## Experiments\n\

\n\

### 1) Evaluate (metrics + confusion matrix)\n\

Windows PowerShell:\n\

* $env:PYTHONPATH = "."\n\
* python experiments/evaluate.py\n
  \n
  Outputs:\n\
* Accuracy, latency, confusion matrix\n\
* Per-category breakdown\n\
* Blocking layer counts\n
  \n\

### 2) Tune Tau (margin threshold sweep)\n\

Windows PowerShell:\n\

* $env:PYTHONPATH = "."\n\
* python experiments/tune_tau.py\n
  \n
  Outputs:\n\
* tau sweep table\n\
* saves CSV: `experiments/tau_sweep_results.csv`\n
  \n
  Interpretation:\n\
* Lower tau (e.g., 0.05): more permissive → higher allow recall, slightly more false allows\n\
* Higher tau (e.g., 0.10+): stricter → fewer accidental allows, but may block more borderline domain prompts\n
  \n\

## Recommended Tau for Enterprise\n\

For enterprise audience, prefer a slightly stricter threshold:\n\

* `layer2_margin_tau = 0.10`\n
  \n
  Reason:\n\
* reduces risk of off-domain prompts passing\n\
* still keeps strong accuracy and cost savings\n
  \n\

## Roadmap\n\

* Add caching of anchor embeddings to reduce warm-start latency\n\
* Add a small allowlist of business-critical generic prompts (e.g., “status update format”)\n\
* Add structured logging + Prometheus metrics\n\
* Add CI pipeline + unit tests for each layer\n
  \n\

## Research & Citation\n\

This project supports a research direction around **FinOps-driven LLM governance** and **domain relevance filtering**.\n
\n
Proposed paper title:\n
SentinelGate: A Hierarchical Cheap-First Guardrail Architecture for Cost-Efficient Domain Relevance\n
\n\

## License\n\

MIT\n
"
