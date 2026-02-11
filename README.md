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

![SentinelGate Architecture Diagram](assets/Architecture%20Diagram.png)

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















# 🛡️ SentinelGate
**Enterprise FinOps Guardrail for LLM Workflows**

**SentinelGate** is a hierarchical "cheap-first" guardrail architecture designed to optimize enterprise LLM costs. By filtering irrelevant, low-value, and off-domain prompts *before* they reach expensive models (like GPT-4), it prevents "token leakage" and ensures AI agents only process valid business queries.

It leverages **Sentence-Transformers**, **Vector Embeddings**, and a **Human-in-the-Loop** memory system to:
- Instantly block spam and trivial noise (<1ms latency)
- Detect semantic chit-chat using dense vector embeddings
- Disambiguate valid domain queries (e.g., Supply Chain) from generic corporate noise (IT/HR)
- Adapt to new use cases via an admin-approved memory store without model retraining

## 🔗 Quick Links

- **📄 Research Paper**: [Read the IEEE Conference Paper](paper/draft.md) *(Coming Soon to arXiv)*
- **🎥 Live Demo**: [Watch the 1-Min Walkthrough](https://drive.google.com/file/d/1Gw1cTGUSmWXGlnL4JnOY5EQeIQ-6rdin/view?usp=sharing)
- **API Docs**: `http://localhost:8000/docs` (Local)
- **GitHub**: [dhrumil10/sentinel-gate](https://github.com/dhrumil10/sentinel-gate)

---

## 📘 Project Description

### 1. The "Cheap-First" Architecture
* **Layer 0 (Heuristic):** $O(1)$ regex checks for null/spam inputs.
* **Layer 1 (Semantic Noise):** Uses `all-MiniLM-L6-v2` to filter generic chit-chat.
* **Layer 2 (Contrastive Domain):** Margin-based scoring to separate valid vs. invalid domains.
* **Layer 2.5 (Adaptive Memory):** Admin-approved vector store for handling edge cases (e.g., IT Helpdesk).

### 2. FinOps Analytics Engine
* **Real-Time ROI:** Tracks "Money Saved" per blocked prompt based on GPT-4 token pricing.
* **Latency Monitoring:** Compares Gate Latency (~10ms) vs. avoided LLM Latency (~2000ms).
* **Efficiency Metrics:** detailed dashboards for Blocked vs. Passed request ratios.

### 3. Infrastructure & Tech Stack
* **FastAPI:** High-performance async Python backend.
* **React (Vite):** Modern dark-mode dashboard for monitoring and admin actions.
* **Docker:** Containerized deployment for cloud scalability.
* **Sentence-Transformers:** Local inference for embedding generation.

---

## 💻 Technologies and Tools

[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-%232496ED?style=for-the-badge&logo=Docker&color=blue&logoColor=white)](https://www.docker.com)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-yellow)](https://huggingface.co/)
[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)

---

## 🚀 Architecture Overview

SentinelGate follows a **cascading cost design** — cheaper checks execute first, more expensive checks later. This ensures that 90% of junk prompts never consume expensive compute resources.

![SentinelGate Architecture Diagram](assets/Architecture%20Diagram.png)

### The 4-Stage Filter Logic:
1.  **Layer 0:** Regex checks (<1ms) → *Blocks "hi", "test"*
2.  **Layer 1:** Semantic Vector Search (~10ms) → *Blocks "tell me a joke"*
3.  **Layer 2:** Contrastive Margin Score (~30ms) → *Blocks "reset my password" (IT)*
4.  **Layer 2.5:** Approved Memory Store (~5ms) → *Allows "IT Helpdesk" if Admin approved*

---

## ⚙️ Setup Instructions

1. **Clone the Repository:**
```bash
git clone [https://github.com/dhrumil10/sentinel-gate.git](https://github.com/dhrumil10/sentinel-gate.git)
cd sentinel-gate
```
2. **Backend Setup (FastAPI):**
```Bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
python -m src.main
```

3. **Frontend Setup (React Dashboard):**
```Bash
cd sentinelgate-ui
npm install
npm run dev
```
4. **Run with Docker (Optional):**
```Bash
docker-compose up --build
```
## 📂 Directory Structuresentinel-gate/
```
├── config.yaml          # Gate configuration (domain, thresholds, anchors)
├── Dockerfile           # Container config
├── requirements.txt     # Python dependencies
├── data/                # Data storage (JSON/CSV)
│   ├── approved_examples.json
│   ├── bypass_requests.json
│   └── sentinelgate_research_data.csv
├── experiments/         # Benchmarking & evaluation scripts
│   ├── evaluate.py
│   ├── generate_data.py
│   └── run_benchmark.py
├── paper/               # Research paper draft
├── sentinelgate-ui/     # React + TypeScript frontend
│   ├── src/
│   │   ├── App.tsx      # Main React component
│   │   └── main.tsx     # Entry point
│   ├── package.json
│   └── vite.config.ts
└── src/                 # Python backend source
    ├── main.py          # FastAPI application
    └── sentinelgate/    # Core package
        ├── approved_store.py
        ├── bypass_store.py
        ├── config.py
        ├── pipeline.py  # Gate logic
        └── similarity.py
```
---
## 📊 Performance 
### Evaluated on a synthetic enterprise dataset (119 prompts).

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

## 👤 Author
# Dhrumil Patel

**MS in Northeastern University, College of Engineering**

[LinkedIn](https://www.linkedin.com/in/dhrumil-patel-10) | [GitHub](https://github.com/dhrumil10)

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
