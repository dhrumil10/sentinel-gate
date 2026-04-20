import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from .similarity import Embedder

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ApprovedExample:
    id: str
    domain: str
    text: str
    embedding: list[float]  # normalized vector
    created_at: str
    approved_by: str

class ApprovedStore:
    """
    JSON-backed approved examples store (demo-friendly).
    Stores normalized embeddings so similarity is just dot product.
    """
    def __init__(self, file_path: str, embedder: Embedder):
        self.path = Path(file_path)
        self.embedder = embedder
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _load(self) -> list[dict[str, Any]]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save(self, rows: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def list(self) -> list[ApprovedExample]:
        return [ApprovedExample(**r) for r in self._load()]

    def add(self, domain: str, text: str, approved_by: str) -> ApprovedExample:
        vec = self.embedder.encode_one(text)  # normalized (your Embedder already does normalize_embeddings=True)
        ex = ApprovedExample(
            id=str(uuid.uuid4()),
            domain=domain,
            text=text,
            embedding=[float(x) for x in vec.tolist()],
            created_at=_now_iso(),
            approved_by=approved_by,
        )
        rows = self._load()
        rows.append(asdict(ex))
        self._save(rows)
        return ex

    def best_match(self, text: str, min_sim: float = 0.87, top_k: int = 3) -> dict[str, Any] | None:
        rows = self._load()
        if not rows:
            return None

        q = self.embedder.encode_one(text)  # (D,)

        # build matrix (N,D)
        M = np.asarray([r["embedding"] for r in rows], dtype=np.float32)
        # dot product since vectors are normalized
        sims = M @ q

        # top-k
        idxs = np.argsort(-sims)[:top_k]
        best_i = int(idxs[0])
        best_sim = float(sims[best_i])

        if best_sim < min_sim:
            return None

        best = rows[best_i]
        return {
            "id": best["id"],
            "domain": best["domain"],
            "text": best["text"],
            "similarity": best_sim,
        }
