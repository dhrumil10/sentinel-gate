
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


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import time
# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from sentinelgate import load_config, SentinelGate

# # --- API INITIALIZATION ---
# app = FastAPI(
#     title="SentinelGate AI Guardrail API",
#     description="Enterprise FinOps Middleware for LLM Prompt Governance",
#     version="1.2.0"
# )

# # Initialize config-driven guardrail engine (loaded once in memory)
# # cfg = load_config()
# from pathlib import Path
# cfg = load_config(str(Path(__file__).resolve().parents[1] / "config.yaml"))

# gate = SentinelGate(cfg)
# from src.sentinelgate.sanitize import sanitize_prompt


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
#     return {"status": "online", "engine": "SentinelGate", "domain": cfg.domain}


# @app.get("/analytics")
# async def get_analytics():
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
#             "tokens_prevented": stats["blocked_count"] * 100  # Approx 100 tokens/prompt
#         },
#         "performance_impact": {
#             "total_latency_saved_seconds": round(stats["latency_saved_ms"] / 1000, 2),
#             "avg_gate_latency_ms": "local"
#         }
#     }


# @app.post("/scan")
# async def scan_prompt(request: PromptRequest):
#     """
#     Primary endpoint to filter prompts.
#     Returns: PASS (send to LLM) or BLOCK (drop request).
#     """
#     # 1) Validate original prompt
#     if not request.prompt or not request.prompt.strip():
#         raise HTTPException(status_code=400, detail="Prompt content cannot be empty")

#     original_prompt = request.prompt

#     # 2) Sanitize (remove greeting/filler prefixes only)
#     clean_prompt = sanitize_prompt(original_prompt)

#     # 3) Validate sanitized prompt (prevents "hey" -> "" edge case)
#     if not clean_prompt or not clean_prompt.strip():
#         raise HTTPException(status_code=400, detail="Prompt content cannot be empty after sanitization")

#     # 4) Run the gate on the sanitized prompt
#     start_time = time.perf_counter()
#     d = gate.check(clean_prompt)
#     gate_latency = (time.perf_counter() - start_time) * 1000

#     # 5) Update Analytics
#     stats["total_scanned"] += 1

#     # 6) Map Decision -> your existing schema
#     if d.decision == "BLOCK":
#         status = "BLOCKED"
#         if d.reason.startswith("junk_"):
#             layer = "L0"
#         elif d.reason == "semantic_noise":
#             layer = "L1"
#         else:
#             layer = "UNKNOWN"
#         reason = d.reason

#     elif d.decision == "ALLOW":
#         status = "PASSED"
#         layer = "L2"
#         reason = d.reason

#     else:
#         # ROUTE: treat as blocked to save tokens (strict mode)
#         status = "BLOCKED"
#         layer = "L2"
#         reason = d.reason

#     if status == "BLOCKED":
#         stats["blocked_count"] += 1
#         stats["money_saved_usd"] += COST_PER_PROMPT_USD
#         stats["latency_saved_ms"] += (AVG_LLM_LATENCY_MS - gate_latency)
#     else:
#         stats["passed_count"] += 1

#     return {
#         "decision": status,
#         "layer_caught": layer,
#         "reason": reason,
#         "gate_latency_ms": round(gate_latency, 2),
#         "action": "SEND_TO_LLM" if status == "PASSED" else "REJECT_REQUEST",
#         "original_prompt": original_prompt,
#         "clean_prompt": clean_prompt,
#         "debug": {
#             "similarity": d.similarity,
#             "margin": d.margin
#         }
#     }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
import time
import sys, os
from pathlib import Path

# Keep your existing sys.path approach
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentinelgate import load_config, SentinelGate, Embedder
from src.sentinelgate.sanitize import sanitize_prompt
from src.sentinelgate.bypass_store import BypassStore
from src.sentinelgate.approved_store import ApprovedStore


# --- API INITIALIZATION ---
app = FastAPI(
    title="SentinelGate AI Guardrail API",
    description="Enterprise FinOps Middleware for LLM Prompt Governance",
    version="1.2.0"
)

# Load config.yaml reliably (repo root)
cfg = load_config(str(Path(__file__).resolve().parents[1] / "config.yaml"))

# ✅ Load embedding model ONCE per process
embedder = Embedder()

# ✅ Create gate using shared embedder (anchors cached inside)
# gate = SentinelGate(cfg, embedder=embedder)


# Stores (JSON files)
DATA_DIR = str(Path(__file__).resolve().parents[1] / "data")
bypass_store = BypassStore(os.path.join(DATA_DIR, "bypass_requests.json"))
approved_store = ApprovedStore(
    file_path=str(Path(__file__).resolve().parents[1] / "data" / "approved_examples.json"),
    embedder=embedder,
)

gate = SentinelGate(cfg, embedder=embedder, approved_store=approved_store)
# --- REAL-TIME ANALYTICS STATE ---
stats = {
    "total_scanned": 0,
    "blocked_count": 0,
    "passed_count": 0,
    "money_saved_usd": 0.0,
    "latency_saved_ms": 0.0
}

COST_PER_PROMPT_USD = 0.0005
AVG_LLM_LATENCY_MS = 2000.0

# Demo “admin auth” (optional). If empty, admin endpoints work without a key.
ADMIN_API_KEY = os.getenv("SENTINELGATE_ADMIN_KEY", "")

class PromptRequest(BaseModel):
    prompt: str

class BypassRequestIn(BaseModel):
    prompt: str
    requested_domain: str = Field(..., examples=["crm", "supply_chain"])
    user_reason: str = Field(..., min_length=3)

class ApproveRequestIn(BaseModel):
    request_id: str
    approved_by: str = Field(..., examples=["admin@company.com"])
    # Optional: admin can rewrite/normalize before storing
    canonical_text: str | None = None
    # Optional: override domain at approval time
    domain: str | None = None

class RejectRequestIn(BaseModel):
    request_id: str
    rejected_by: str
    note: str | None = None

# --- ENDPOINTS ---
def _require_admin(x_admin_key: str | None):
    if ADMIN_API_KEY and x_admin_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized (bad admin key)")

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
            "tokens_prevented": stats["blocked_count"] * 100
        },
        "performance_impact": {
            "total_latency_saved_seconds": round(stats["latency_saved_ms"] / 1000, 2),
            "avg_gate_latency_ms": "local"
        }
    }


# @app.post("/scan")
# async def scan_prompt(request: PromptRequest):
#     """
#     Primary endpoint to filter prompts.
#     Returns: PASS (send to LLM) or BLOCK (drop request).
#     """
#     if not request.prompt or not request.prompt.strip():
#         raise HTTPException(status_code=400, detail="Prompt content cannot be empty")

#     original_prompt = request.prompt

#     clean_prompt = sanitize_prompt(original_prompt)

#     if not clean_prompt or not clean_prompt.strip():
#         raise HTTPException(status_code=400, detail="Prompt content cannot be empty after sanitization")

#     start_time = time.perf_counter()
#     d = gate.check(clean_prompt)
#     gate_latency = (time.perf_counter() - start_time) * 1000

#     stats["total_scanned"] += 1

#     if d.decision == "BLOCK":
#         status = "BLOCKED"
#         if d.reason.startswith("junk_"):
#             layer = "L0"
#         elif d.reason in ("semantic_noise", "mixed_intent"):
#             layer = "L1"
#         # elif d.reason == "semantic_noise":
#         #     layer = "L1"
#         else:
#             layer = "UNKNOWN"
#         reason = d.reason

#     elif d.decision == "ALLOW":
#         status = "PASSED"
#         layer = "L2"
#         reason = d.reason

#     else:
#         status = "BLOCKED"
#         layer = "L2"
#         reason = d.reason

#     if status == "BLOCKED":
#         stats["blocked_count"] += 1
#         stats["money_saved_usd"] += COST_PER_PROMPT_USD
#         stats["latency_saved_ms"] += (AVG_LLM_LATENCY_MS - gate_latency)
#     else:
#         stats["passed_count"] += 1

#     return {
#         "decision": status,
#         "layer_caught": layer,
#         "reason": reason,
#         "gate_latency_ms": round(gate_latency, 2),
#         "action": "SEND_TO_LLM" if status == "PASSED" else "REJECT_REQUEST",
#         "original_prompt": original_prompt,
#         "clean_prompt": clean_prompt,
#         "debug": {
#             "similarity": d.similarity,
#             "margin": d.margin
#         }
#     }

# @app.post("/scan")
# async def scan_prompt(request: PromptRequest):
#     if not request.prompt or not request.prompt.strip():
#         raise HTTPException(status_code=400, detail="Prompt content cannot be empty")

#     original_prompt = request.prompt
#     clean_prompt = sanitize_prompt(original_prompt)

#     if not clean_prompt or not clean_prompt.strip():
#         raise HTTPException(status_code=400, detail="Prompt content cannot be empty after sanitization")

#     start_time = time.perf_counter()
#     print("approved_count =", getattr(gate, "approved_count", None))
#     d = gate.check(clean_prompt)
#     gate_latency = (time.perf_counter() - start_time) * 1000

#     stats["total_scanned"] += 1

#     # Default mapping (same as you already do)
#     status = None
#     layer = None
#     reason = d.reason

#     if d.decision == "BLOCK":
#         status = "BLOCKED"
#         if d.reason.startswith("junk_"):
#             layer = "L0"
#         elif d.reason == "semantic_noise":
#             layer = "L1"
#         else:
#             layer = "UNKNOWN"

#     elif d.decision == "ALLOW":
#         status = "PASSED"
#         layer = "L2"

#     else:
#         # ROUTE => strict mode: currently BLOCKED
#         status = "BLOCKED"
#         layer = "L2"

#         # ✅ Layer 2.5: check approved examples to auto-pass/route
#         match = approved_store.best_match(
#             clean_prompt,
#             min_sim=float(os.getenv("SENTINELGATE_APPROVED_MIN_SIM", "0.87")),
#             top_k=int(os.getenv("SENTINELGATE_APPROVED_TOP_K", "3")),
#         )

#         if match:
#             status = "PASSED"
#             layer = "L2.5"
#             reason = "approved_match"

#     if status == "BLOCKED":
#         stats["blocked_count"] += 1
#         stats["money_saved_usd"] += COST_PER_PROMPT_USD
#         stats["latency_saved_ms"] += (AVG_LLM_LATENCY_MS - gate_latency)
#     else:
#         stats["passed_count"] += 1

#     # attach match info (if any)
#     # approved_match = None
#     "approved_match": getattr(d, "approved_match", None)
#     if layer == "L2.5":
#         approved_match = approved_store.best_match(clean_prompt)

#     return {
#         "decision": status,
#         "layer_caught": layer,
#         "reason": reason,
#         "gate_latency_ms": round(gate_latency, 2),
#         "action": "SEND_TO_LLM" if status == "PASSED" else "REJECT_REQUEST",
#         "original_prompt": original_prompt,
#         "clean_prompt": clean_prompt,
#         "approved_match": approved_match,  # {id, domain, text, similarity} or null
#         "debug": {
#             "similarity": d.similarity,
#             "margin": d.margin
#         }
#     }
@app.post("/scan")
async def scan_prompt(request: PromptRequest):
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt content cannot be empty")

    original_prompt = request.prompt
    clean_prompt = sanitize_prompt(original_prompt)

    if not clean_prompt or not clean_prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt content cannot be empty after sanitization")

    start_time = time.perf_counter()
    d = gate.check(clean_prompt)
    gate_latency = (time.perf_counter() - start_time) * 1000

    stats["total_scanned"] += 1

    # default mapping
    reason = d.reason
    approved_match = None

    if d.decision == "BLOCK":
        status = "BLOCKED"
        if d.reason.startswith("junk_"):
            layer = "L0"
        elif d.reason == "semantic_noise":
            layer = "L1"
        else:
            layer = "UNKNOWN"

    elif d.decision == "ALLOW":
        status = "PASSED"
        layer = "L2"

        # if it was allowed due to approved match, show it
        if d.reason == "approved_match":
            layer = "L2.5"
            approved_match = getattr(d, "approved_match", None)

    else:
        # ROUTE => strict mode: treat blocked
        status = "BLOCKED"
        layer = "L2"

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
        "original_prompt": original_prompt,
        "clean_prompt": clean_prompt,
        "approved_match": approved_match,
        "debug": {
            "similarity": d.similarity,
            "margin": d.margin
        }
    }

@app.post("/bypass/request")
async def create_bypass_request(body: BypassRequestIn):
    original = body.prompt
    clean = sanitize_prompt(original)

    if not clean or not clean.strip():
        raise HTTPException(status_code=400, detail="Prompt became empty after sanitization")

    req = bypass_store.create(
        requested_domain=body.requested_domain.strip().lower(),
        user_reason=body.user_reason.strip(),
        original_prompt=original,
        clean_prompt=clean,
    )
    return {"status": "ok", "request_id": req.id, "clean_prompt": req.clean_prompt}


@app.get("/admin/bypass/requests")
async def list_bypass_requests(status: str | None = None, x_admin_key: str | None = Header(default=None)):
    _require_admin(x_admin_key)
    s = status.upper() if status else None
    if s and s not in {"PENDING", "APPROVED", "REJECTED"}:
        raise HTTPException(status_code=400, detail="Invalid status")
    return {"items": [r.__dict__ for r in bypass_store.list(status=s)]}


@app.post("/admin/bypass/approve")
async def approve_bypass_request(body: ApproveRequestIn, x_admin_key: str | None = Header(default=None)):
    _require_admin(x_admin_key)

    req = bypass_store.get(body.request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req.status != "PENDING":
        raise HTTPException(status_code=409, detail=f"Request is already {req.status}")

    domain = (body.domain or req.requested_domain).strip().lower()
    text = (body.canonical_text or req.clean_prompt).strip()

    if not text:
        raise HTTPException(status_code=400, detail="canonical_text cannot be empty")

    ex = approved_store.add(domain=domain, text=text, approved_by=body.approved_by.strip())
    gate.refresh_approved()

    bypass_store.update_status(
        request_id=req.id,
        status="APPROVED",
        reviewed_by=body.approved_by.strip(),
        review_note=f"Stored approved example_id={ex.id} domain={domain}",
    )
    
    return {"status": "ok", "approved_example": asdict_like(ex)}


@app.post("/admin/bypass/reject")
async def reject_bypass_request(body: RejectRequestIn, x_admin_key: str | None = Header(default=None)):
    _require_admin(x_admin_key)

    req = bypass_store.get(body.request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req.status != "PENDING":
        raise HTTPException(status_code=409, detail=f"Request is already {req.status}")

    updated = bypass_store.update_status(
        request_id=req.id,
        status="REJECTED",
        reviewed_by=body.rejected_by.strip(),
        review_note=body.note,
    )
    return {"status": "ok", "request": updated.__dict__ if updated else None}


def asdict_like(ex):
    # small helper to avoid importing dataclasses.asdict in main
    return {
        "id": ex.id,
        "domain": ex.domain,
        "text": ex.text,
        "created_at": ex.created_at,
        "approved_by": ex.approved_by,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
