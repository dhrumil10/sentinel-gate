from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .filters import SentinelGate  # Import the logic you already built
import time

# Initialize FastAPI app
app = FastAPI(
    title="SentinelGate AI Guardrail API",
    description="A lightweight API to filter LLM prompts before they hit expensive models.",
    version="1.0.0"
)

# Initialize the Gate (Loaded once at startup)
gate = SentinelGate()

# Define the request structure
class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "SentinelGate API is Online", "status": "Ready"}

@app.post("/scan")
async def scan_prompt(request: PromptRequest):
    """
    Scans a prompt and returns a PASS or BLOCK decision.
    """
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    start_time = time.time()
    
    # Run our 3-Layer Filter logic
    result = gate.scan(request.prompt)
    
    latency_ms = (time.time() - start_time) * 1000

    return {
        "decision": result["status"],
        "layer_analyzed": result["layer"],
        "reason": result["reason"],
        "latency_ms": round(latency_ms, 2)
    }

if __name__ == "__main__":
    import uvicorn
    # Run server on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)