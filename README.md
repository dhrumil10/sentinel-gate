# SentinelGate: Cost-Efficient LLM Guardrails 🛡️

**A Hierarchical "Cheap-First" Architecture for Enterprise AI Governance and FinOps.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Accuracy](https://img.shields.io/badge/accuracy-92.44%25-green)
![Latency](https://img.shields.io/badge/avg_latency-~10ms-brightgreen)

---

## 📌 Abstract

SentinelGate is a lightweight **pre-flight LLM guardrail system** designed to reduce enterprise AI costs by **40%+** by blocking irrelevant, noisy, and off-domain prompts *before* they reach expensive LLM APIs.

Unlike traditional guardrails focused on safety (toxicity, PII, policy), SentinelGate focuses on:

- **FinOps efficiency**
- **Domain relevance**
- **Enterprise prompt hygiene**

The system uses a **hierarchical cheap-first pipeline** combined with an **approved bypass memory (human-in-the-loop)** to achieve both **cost control** and **organizational flexibility**.

---

## 🚀 Architecture Overview

SentinelGate follows a **cascading cost design** — cheaper checks execute first, more expensive checks later. This ensures that 90% of junk prompts never consume expensive compute resources.

![SentinelGate Architecture Diagram](Gemini_Generated_Image_s2k59is2k59is2k5.jpg)

### Layered Pipeline

### **L0 — Heuristic / Regex Junk Filter**
- Blocks empty prompts, greetings, test messages
- Examples: `hi`, `test`, `???`
- Latency: `< 1 ms`

### **L1 — Semantic Noise Filter**
- Uses `sentence-transformers/all-MiniLM-L6-v2`
- Blocks chitchat / non-work content
- Examples: `tell me a joke`, `write a poem`
- Latency: `~8–10 ms`

### **L2 — Contrastive Domain Gate**
- **Margin-based similarity check:**
  `margin = sim(domain_positive) - sim(domain_negative)`
- Distinguishes **Supply Chain work** from **generic corporate work** (HR / IT / Admin).
- Passes if `margin >= tau`.

### **L2.5 — Approved Bypass Memory (NEW)**
- Human-approved off-domain examples are stored with embeddings
- Similar future prompts auto-pass **without touching LLM**
- Enables:
- Domain expansion
- Exception handling
- Enterprise flexibility

---

## 🔧 Tau Threshold (Layer 2)
The `tau` parameter controls the strictness of the Domain Gate.
- **Lower `tau`**: Higher recall (more permissive).
- **Higher `tau`**: Stricter domain enforcement.

**Recommended Enterprise Value:** `layer2_margin_tau: 0.10`

**Recommended enterprise value**:
- Distinguishes **Supply Chain work** from **generic corporate work** (HR / IT / Admin)
- Passes if `margin >= tau`

### **L2.5 — Approved Bypass Memory (NEW)**
- Human-approved off-domain examples are stored with embeddings
- Similar future prompts auto-pass **without touching LLM**
- Enables:
- Domain expansion
- Exception handling
- Enterprise flexibility

---

## 🔧 Tau Threshold (Layer 2)

- Lower `tau` → higher recall (more permissive)
- Higher `tau` → stricter domain enforcement

**Recommended enterprise value**:

---
### layer2_margin_tau: 0.10

Both `original_prompt` and `clean_prompt` are returned for transparency.

---

## 🧠 Human-in-the-Loop Bypass Flow (NEW)

SentinelGate supports **admin-reviewed domain expansion**.

### Workflow

1. User submits an off-domain prompt
2. Prompt is blocked at L2
3. User requests bypass: `POST /bypass/request`
4. Admin reviews & approves: `POST /admin/bypass/approve`

### POST /admin/bypass/approve

5. Canonical prompt is embedded & stored
6. Future similar prompts auto-pass at **L2.5**

This allows SentinelGate to **learn organizational exceptions safely**.



## 🖥️ Web UI (React + Vite)

SentinelGate includes a demo UI for:
- Live prompt scanning
- Layer visualization (L0 / L1 / L2 / L2.5)
- Debug metrics (similarity, margin)
- Approved bypass visibility
- History tracking

### Run UI
```bash
cd sentinelgate-ui
npm install
npm run dev
```
### Open:
```arduino
http://localhost:5173
```

## 📊 Benchmark Results

Evaluated on a synthetic enterprise dataset (119 prompts).
| Metric | Result |
| :--- | :--- |
| **Overall Accuracy** | **92.44%** |
| **Junk Blocking** | 100.0% |
| **Generic Blocking** | 100.0% |
| **Domain Accuracy** | 80.0% |
| **Avg Gate Latency** | ~9.65 ms |
| **Est. Cost Savings** | ~$1.26 per 100 requests |

**Example ```/scan``` Response**
```json
{
  "decision": "PASSED",
  "layer_caught": "L2.5",
  "reason": "approved_match",
  "gate_latency_ms": 39.04,
  "action": "SEND_TO_LLM",
  "original_prompt": "vpn is not working on my corporate laptop",
  "clean_prompt": "vpn is not working on my corporate laptop",
  "approved_match": {
    "domain": "it_helpdesk",
    "similarity": 0.83
  },
  "debug": {
    "similarity": 0.83,
    "margin": null
  }
}
```

## 🛠️ Installation
```bash
git clone [https://github.com/dhrumil10/sentinel-gate.git](https://github.com/dhrumil10/sentinel-gate.git)
cd sentinel-gate
python -m venv venv
```

* **Windows:**
    ```bash
    venv\Scripts\activate
    ```
* **Mac / Linux:**
    ```bash
    source venv/bin/activate
    ```
```bash
pip install -r requirements.txt
```

## 🚀 Run Backend  
```bash
# Windows
$env:PYTHONPATH="."
uvicorn src.main:app --reload

# Mac/Linux
export PYTHONPATH="."
uvicorn src.main:app --reload
```
**Swagger:-**
```arduino
http://127.0.0.1:8000/docs
```

## 🧪 Experiments
**Evaluate:-**
```bash
python experiments/evaluate.py
```
**Tune Tau:-**
```bash
python experiments/tune_tau.py
```
**Outputs:-**
```bash
experiments/tau_sweep_results.csv
```
## ⚙️ Configuration
SentinelGate is fully **config-driven** via `config.yaml`, allowing for real-time adjustments without code changes:
- **Domain Definition**: Define "In-Domain" vs. "Off-Domain" scopes.
- **Anchor Phrases**: Centralize positive and negative semantic anchors.
- **Thresholds**: Fine-tune `layer2_margin_tau` for precision.
- **Noise Filters**: Configure L1 filters to block "junk" or "chitchat."

## 📄 Research Direction

### This project supports research into:
  - FinOps-driven LLM governance
  - Domain relevance filtering
  - Human-in-the-loop AI control
  - Cost-aware AI system design

## 🎥 Demo Video

See the guardrail in action: blocking junk, filtering off-domain noise, and handling admin approvals in real-time.

[Watch the Full Demo](https://drive.google.com/file/d/1Gw1cTGUSmWXGlnL4JnOY5EQeIQ-6rdin/view?usp=sharing)
