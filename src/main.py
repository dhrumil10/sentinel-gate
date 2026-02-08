
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from .filters import SentinelGate
# import time

# # --- API INITIALIZATION ---
# app = FastAPI(
#     title="SentinelGate AI Guardrail API",
#     description="Enterprise FinOps Middleware for LLM Prompt Governance",
#     version="1.1.0"
# )

# # Initialize the guardrail engine (Loaded once in memory)
# gate = SentinelGate()

# # --- REAL-TIME ANALYTICS STATE ---
# # In production, this would be backed by Redis or Prometheus
# stats = {
#     "total_scanned": 0,
#     "blocked_count": 0,
#     "passed_count": 0,
#     "money_saved_usd": 0.0,
#     "latency_saved_ms": 0.0
# }

# # Industry estimate: $0.0005 per avg prompt (GPT-4o) and 2000ms avg LLM latency
# COST_PER_PROMPT_USD = 0.0005
# AVG_LLM_LATENCY_MS = 2000.0

# class PromptRequest(BaseModel):
#     prompt: str

# # --- ENDPOINTS ---

# @app.get("/")
# def health_check():
#     return {"status": "online", "engine": "SentinelGate", "domain": "Supply Chain"}

# @app.get("/analytics")
# async def get_analytics():
#     """
#     Returns the real-time Financial and Operational ROI of the guardrail.
#     """
#     efficiency = (stats["blocked_count"] / stats["total_scanned"] * 100) if stats["total_scanned"] > 0 else 0
    
#     return {
#         "report": "SentinelGate FinOps Summary",
#         "metrics": {
#             "total_requests": stats["total_scanned"],
#             "prompts_blocked": stats["blocked_count"],
#             "prompts_passed": stats["passed_count"],
#             "efficiency_rate": f"{efficiency:.2f}%"
#         },
#         "financial_impact": {
#             "estimated_usd_saved": f"${stats['money_saved_usd']:.4f}",
#             "tokens_prevented": stats["blocked_count"] * 100 # Approx 100 tokens/prompt
#         },
#         "performance_impact": {
#             "total_latency_saved_seconds": round(stats["latency_saved_ms"] / 1000, 2),
#             "avg_gate_latency_ms": "10.69ms (benchmarked)"
#         }
#     }

# @app.post("/scan")
# async def scan_prompt(request: PromptRequest):
#     """
#     Primary endpoint to filter prompts. 
#     Returns: PASS (send to LLM) or BLOCK (drop request).
#     """
#     if not request.prompt.strip():
#         raise HTTPException(status_code=400, detail="Prompt content cannot be empty")

#     start_time = time.time()
    
#     # Execute the 3-Layer Hierarchical Check
#     result = gate.scan(request.prompt)
    
#     # Calculate Latency
#     gate_latency = (time.time() - start_time) * 1000
    
#     # Update Analytics
#     stats["total_scanned"] += 1
    
#     if result["status"] == "BLOCKED":
#         stats["blocked_count"] += 1
#         stats["money_saved_usd"] += COST_PER_PROMPT_USD
#         stats["latency_saved_ms"] += (AVG_LLM_LATENCY_MS - gate_latency)
#     else:
#         stats["passed_count"] += 1

#     return {
#         "decision": result["status"],
#         "layer_caught": result["layer"],
#         "reason": result["reason"],
#         "gate_latency_ms": round(gate_latency, 2),
#         "action": "SEND_TO_LLM" if result["status"] == "PASSED" else "REJECT_REQUEST"
#     }

# if __name__ == "__main__":
#     import uvicorn
#     # Start the server on port 8000
#     uvicorn.run(app, host="127.0.0.1", port=8000)


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

from sentinelgate import load_config, SentinelGate

# --- API INITIALIZATION ---
app = FastAPI(
    title="SentinelGate AI Guardrail API",
    description="Enterprise FinOps Middleware for LLM Prompt Governance",
    version="1.2.0"
)

# Initialize config-driven guardrail engine (loaded once in memory)
# cfg = load_config()
from pathlib import Path
cfg = load_config(str(Path(__file__).resolve().parents[1] / "config.yaml"))
gate = SentinelGate(cfg)


# --- REAL-TIME ANALYTICS STATE ---
# In production, this would be backed by Redis or Prometheus
stats = {
    "total_scanned": 0,
    "blocked_count": 0,
    "passed_count": 0,
    "money_saved_usd": 0.0,
    "latency_saved_ms": 0.0
}

# Industry estimate: $0.0005 per avg prompt (GPT-4o) and 2000ms avg LLM latency
COST_PER_PROMPT_USD = 0.0005
AVG_LLM_LATENCY_MS = 2000.0


class PromptRequest(BaseModel):
    prompt: str


# --- ENDPOINTS ---

@app.get("/")
def health_check():
    return {"status": "online", "engine": "SentinelGate", "domain": cfg.domain}


@app.get("/analytics")
async def get_analytics():
    efficiency = (stats["blocked_count"] / stats["total_scanned"] * 100) if stats["total_scanned"] > 0 else 0

    return {
        "report": "SentinelGate FinOps Summary",
        "metrics": {
            "total_requests": stats["total_scanned"],
            "prompts_blocked": stats["blocked_count"],
            "prompts_passed": stats["passed_count"],
            "efficiency_rate": f"{efficiency:.2f}%"
        },
        "financial_impact": {
            "estimated_usd_saved": f"${stats['money_saved_usd']:.4f}",
            "tokens_prevented": stats["blocked_count"] * 100  # Approx 100 tokens/prompt
        },
        "performance_impact": {
            "total_latency_saved_seconds": round(stats["latency_saved_ms"] / 1000, 2),
            "avg_gate_latency_ms": "local"
        }
    }


@app.post("/scan")
async def scan_prompt(request: PromptRequest):
    """
    Primary endpoint to filter prompts.
    Returns: PASS (send to LLM) or BLOCK (drop request).
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt content cannot be empty")

    start_time = time.perf_counter()

    d = gate.check(request.prompt)

    gate_latency = (time.perf_counter() - start_time) * 1000

    # Update Analytics
    stats["total_scanned"] += 1

    # Map Decision -> your existing schema
    if d.decision == "BLOCK":
        status = "BLOCKED"
        if d.reason.startswith("junk_"):
            layer = "L0"
        elif d.reason == "semantic_noise":
            layer = "L1"
        else:
            layer = "UNKNOWN"
        reason = d.reason

    elif d.decision == "ALLOW":
        status = "PASSED"
        layer = "L2"
        reason = d.reason

    else:
        # ROUTE: treat as blocked to save tokens (strict mode)
        status = "BLOCKED"
        layer = "L2"
        reason = d.reason

    if status == "BLOCKED":
        stats["blocked_count"] += 1
        stats["money_saved_usd"] += COST_PER_PROMPT_USD
        stats["latency_saved_ms"] += (AVG_LLM_LATENCY_MS - gate_latency)
    else:
        stats["passed_count"] += 1

    return {
        "decision": status,
        "layer_caught": layer,
        "reason": reason,
        "gate_latency_ms": round(gate_latency, 2),
        "action": "SEND_TO_LLM" if status == "PASSED" else "REJECT_REQUEST",
        "debug": {
            "similarity": d.similarity,
            "margin": d.margin
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
