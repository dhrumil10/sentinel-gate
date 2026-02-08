import re
import numpy as np
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
from .config import Config
from .similarity import max_sim

@dataclass
class Decision:
    decision: str  # ALLOW | BLOCK | ROUTE | REWRITE
    reason: str
    message: str
    similarity: float | None = None
    margin: float | None = None

def normalize(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t

def layer0_junk(prompt: str, cfg: Config) -> Decision | None:
    raw = prompt.strip()
    t = normalize(prompt)

    if not t:
        return Decision("BLOCK", "junk_empty", "Please share your work task (goal + context).")

    # exact junk (includes short acknowledgements)
    if t in set(cfg.layer0.junk_exact):
        return Decision("BLOCK", "junk_exact", "Please ask a work-related question with a goal + context.")

    # too short
    if len(t.split()) < cfg.layer0.min_tokens:
        return Decision("BLOCK", "junk_too_short", "Please add more context (goal + details).")

    # regex junk (punctuation/emojis only etc.)
    for pat in cfg.layer0.junk_regex:
        if re.match(pat, raw):
            return Decision("BLOCK", "junk_regex", "Please ask a work-related question with a goal + context.")

    return None

class SentinelGate:
    def __init__(self, cfg: Config, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.cfg = cfg
        self.embedder = SentenceTransformer(model_name)

        self.noise_anchors = self._embed_list(cfg.layer1_noise_anchors)
        self.pos_anchors = self._embed_list(cfg.layer2_domain_positive_anchors)
        self.neg_anchors = self._embed_list(cfg.layer2_domain_negative_anchors)

    def _embed_list(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, 384), dtype=np.float32)
        embs = self.embedder.encode(texts, normalize_embeddings=True)
        return np.array(embs, dtype=np.float32)

    def _embed_prompt(self, prompt: str) -> np.ndarray:
        emb = self.embedder.encode([prompt], normalize_embeddings=True)[0]
        return np.array(emb, dtype=np.float32)

    def check(self, prompt: str) -> Decision:
        # Layer 0: cheap junk filter
        d0 = layer0_junk(prompt, self.cfg)
        if d0:
            return d0

        p = self._embed_prompt(prompt)

        # Layer 1: semantic noise
        noise = max_sim(p, self.noise_anchors)
        if noise > self.cfg.thresholds.layer1_noise_max_sim:
            return Decision(
                "BLOCK",
                "semantic_noise",
                "This looks like non-work chatter. Please ask a work task (inventory/shipments/vendors/warehouse/forecasting).",
                similarity=noise,
            )

        # Layer 2: contrastive domain gate (pos vs neg + margin)
        pos = max_sim(p, self.pos_anchors)
        neg = max_sim(p, self.neg_anchors)
        margin = pos - neg

        if margin >= self.cfg.thresholds.layer2_margin_tau:
            return Decision("ALLOW", "domain_match", "Allowed", similarity=pos, margin=margin)

        return Decision(
            "ROUTE",
            "off_domain",
            "This seems outside supply-chain scope. Rephrase with supply-chain context or route to a general assistant.",
            similarity=pos,
            margin=margin,
        )
