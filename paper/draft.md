# SentinelGate: A Three-Stage Hierarchical Guardrail Architecture for Cost-Efficient Domain Adaptation in LLM Workflows

**Author:** Dhrumil Patel  
**Date:** February 2026  
**Subject:** Applied AI / FinOps  

## 1. Abstract
The rapid adoption of Large Language Models (LLMs) has introduced significant operational costs. This paper introduces **SentinelGate**, a hierarchical gating system designed to filter irrelevant queries before model invocation. Utilizing a three-layer architecture—heuristic rules, semantic noise filtering, and contrastive domain-anchor disambiguation—SentinelGate achieves an overall accuracy of **92.44%** with a mean latency of **10.69ms**, providing a scalable framework for enterprise FinOps.

## 2. Introduction
In specialized domains like Supply Chain Management, LLMs often process "Token Leakage"—user prompts that are low-value (chitchat) or irrelevant. SentinelGate proposes a "Cheap-First" alternative. By cascading from $O(1)$ regex checks to $O(n)$ small-model vector similarities, we protect expensive infrastructure at near-zero performance cost.

## 3. Methodology
The system follows a cascading logic to minimize computational overhead:

### 3.1 Layer 0: Heuristic Pre-Filtering (Regex)
Identifies null inputs and trivial strings (e.g., "test", "hi") in $O(1)$ time.

### 3.2 Layer 1: Semantic Noise Filtering
Uses `all-MiniLM-L6-v2` to map inputs to vector space. If the Cosine Similarity $S$ against "Junk Anchors" (e.g., "tell me a joke") exceeds $0.50$, the prompt is blocked.

### 3.3 Layer 2: Contrastive Domain-Anchor Disambiguation
Calculates similarity against **Positive Anchors** (Supply Chain) and **Negative Anchors** (IT/HR). A prompt is allowed only if its similarity to the Positive set is significantly higher than the Negative set.

## 4. Experimental Results
Tested against 119 prompts:
* **Overall Accuracy:** 92.44%
* **Mean Latency:** 10.69 ms (Terminal) / 35.46 ms (API)
* **Junk/Generic Rejection:** 100%
* **Domain Recall:** 80%

## 5. Conclusion & Future Work
SentinelGate demonstrates that embedding-based guardrails effectively govern LLM usage. Future work will focus on **Dynamic Anchor Updating** to improve domain recall and **Multi-Model Routing** to send generic queries to smaller, cheaper models.