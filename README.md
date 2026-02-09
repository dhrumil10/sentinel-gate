# SentinelGate: Cost-Efficient LLM Guardrails 🛡️

**A Hierarchical "Cheap-First" Architecture for Enterprise AI Governance.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Accuracy](https://img.shields.io/badge/accuracy-92.4%25-green)
![Latency](https://img.shields.io/badge/latency-10ms-brightgreen)

## 📌 Abstract
SentinelGate is a lightweight, pre-flight guardrail system designed to reduce Enterprise LLM costs by **40%+**. It prevents "Hallucination Baiting" and blocks irrelevant queries *before* they hit expensive APIs like GPT-4.

Unlike standard guardrails that focus on safety (hate speech), SentinelGate focuses on **FinOps and Domain Relevance**. It uses a novel 3-stage filtering pipeline to distinguish between "Valid Supply Chain Queries" and "Generic Corporate Noise" (like IT support tickets) with **92% accuracy**.

## 🚀 The Architecture
The system uses a "Cascading Cost" design. Cheap checks run first; expensive checks run last.

1.  **Layer 0 (Regex/Heuristic):** Instantly blocks spam ("hi", "test") in <1ms.
2.  **Layer 1 (Semantic Noise):** Uses `all-MiniLM-L6-v2` to detect chitchat ("Tell me a joke") in ~10ms.
3.  **Layer 2 (Contrastive Domain):** A novel "Positive vs. Negative Anchor" check to distinguish Domain Work (Supply Chain) from Generic Work (HR/IT).

## 📊 Benchmark Results
Tested on a synthetic dataset of 119 enterprise prompts.

| Metric | Result |
| :--- | :--- |
| **Overall Accuracy** | **92.44%** |
| **Junk Blocking** | 100.0% |
| **Generic Blocking** | 100.0% |
| **Avg Latency** | 10.69 ms |
| **Est. Cost Savings** | ~$1.26 per 100 requests |

## 🛠️ Installation & Usage

### 1. Clone the Repo
```bash
git clone [https://github.com/YOUR_USERNAME/sentinel-gate.git](https://github.com/YOUR_USERNAME/sentinel-gate.git)
cd sentinel-gate
```

### 2. Install Dependencies
```Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Run the Benchmark
```Bash
python experiments/run_benchmark.py
```
# 📄 Research & Citation
This project implements the architecture described in the paper:

"SentinelGate: A Two-Stage Hierarchical Guardrail Architecture for Cost-Efficient Domain Adaptation."
