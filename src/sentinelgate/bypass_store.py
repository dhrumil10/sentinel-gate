import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

Status = Literal["PENDING", "APPROVED", "REJECTED"]

@dataclass
class BypassRequest:
    id: str
    status: Status
    requested_domain: str
    user_reason: str
    original_prompt: str
    clean_prompt: str
    created_at: str

    reviewed_at: str | None = None
    reviewed_by: str | None = None
    review_note: str | None = None

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class BypassStore:
    """
    Simple JSON-backed store for bypass requests.
    - No dependencies
    - Good for demo / local
    """
    def __init__(self, file_path: str):
        self.path = Path(file_path)
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

    def create(
        self,
        requested_domain: str,
        user_reason: str,
        original_prompt: str,
        clean_prompt: str,
    ) -> BypassRequest:
        req = BypassRequest(
            id=str(uuid.uuid4()),
            status="PENDING",
            requested_domain=requested_domain,
            user_reason=user_reason,
            original_prompt=original_prompt,
            clean_prompt=clean_prompt,
            created_at=_now_iso(),
        )
        rows = self._load()
        rows.append(asdict(req))
        self._save(rows)
        return req

    def list(self, status: Status | None = None) -> list[BypassRequest]:
        rows = self._load()
        out: list[BypassRequest] = []
        for r in rows:
            if status and r.get("status") != status:
                continue
            out.append(BypassRequest(**r))
        # newest first
        out.sort(key=lambda x: x.created_at, reverse=True)
        return out

    def get(self, request_id: str) -> BypassRequest | None:
        for r in self._load():
            if r.get("id") == request_id:
                return BypassRequest(**r)
        return None

    def update_status(
        self,
        request_id: str,
        status: Status,
        reviewed_by: str,
        review_note: str | None = None,
    ) -> BypassRequest | None:
        rows = self._load()
        updated = None
        for r in rows:
            if r.get("id") == request_id:
                r["status"] = status
                r["reviewed_by"] = reviewed_by
                r["review_note"] = review_note
                r["reviewed_at"] = _now_iso()
                updated = BypassRequest(**r)
                break
        if updated:
            self._save(rows)
        return updated
