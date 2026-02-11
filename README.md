
# 🛡️ SentinelGate
**Enterprise FinOps Guardrail for LLM Workflows**

**SentinelGate** is a hierarchical "cheap-first" guardrail architecture designed to optimize enterprise LLM costs. By filtering irrelevant, low-value, and off-domain prompts *before* they reach expensive models (like GPT-4), it prevents "token leakage" and ensures AI agents only process valid business queries.

It leverages **Sentence-Transformers**, **Vector Embeddings**, and a **Human-in-the-Loop** memory system to:
- Instantly block spam and trivial noise (<1ms latency)
- Detect semantic chit-chat using dense vector embeddings
- Disambiguate valid domain queries (e.g., Supply Chain) from generic corporate noise (IT/HR)
- Adapt to new use cases via an admin-approved memory store without model retraining

## 🔗 Quick Links

- **📄 Research Paper**: [Read the IEEE Conference Paper](paper/SentinelGate.pdf) *(Coming Soon to arXiv)*
- **🎥 Live Demo**: [Watch the 11-Min Walkthrough](https://drive.google.com/file/d/1Gw1cTGUSmWXGlnL4JnOY5EQeIQ-6rdin/view?usp=sharing)
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
