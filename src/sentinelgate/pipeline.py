
# import re
# import numpy as np
# from dataclasses import dataclass
# from .config import Config
# from .similarity import max_sim, Embedder

# @dataclass
# class Decision:
#     decision: str  # ALLOW | BLOCK | ROUTE | REWRITE
#     reason: str
#     message: str
#     similarity: float | None = None
#     margin: float | None = None

# def normalize(text: str) -> str:
#     t = text.strip().lower()
#     t = re.sub(r"\s+", " ", t)
#     return t

# def layer0_junk(prompt: str, cfg: Config) -> Decision | None:
#     raw = prompt.strip()
#     t = normalize(prompt)

#     if not t:
#         return Decision("BLOCK", "junk_empty", "Please share your work task (goal + context).")

#     if t in set(cfg.layer0.junk_exact):
#         return Decision("BLOCK", "junk_exact", "Please ask a work-related question with a goal + context.")

#     if len(t.split()) < cfg.layer0.min_tokens:
#         return Decision("BLOCK", "junk_too_short", "Please add more context (goal + details).")

#     for pat in cfg.layer0.junk_regex:
#         if re.match(pat, raw):
#             return Decision("BLOCK", "junk_regex", "Please ask a work-related question with a goal + context.")

#     return None

# class SentinelGate:
#     """
#     Config-driven hierarchical gate.
#     Uses injected Embedder so the model loads once and can be reused.
#     """
#     def __init__(self, cfg: Config, embedder: Embedder | None = None):
#         self.cfg = cfg
#         self.embedder = embedder or Embedder()

#         # Cache anchor embeddings once
#         self.noise_anchors = self.embedder.encode_list(cfg.layer1_noise_anchors)
#         self.pos_anchors = self.embedder.encode_list(cfg.layer2_domain_positive_anchors)
#         self.neg_anchors = self.embedder.encode_list(cfg.layer2_domain_negative_anchors)

#     def _embed_prompt(self, prompt: str) -> np.ndarray:
#         return self.embedder.encode_one(prompt)

#     def check(self, prompt: str) -> Decision:
#         # Layer 0: cheap junk filter
#         d0 = layer0_junk(prompt, self.cfg)
#         if d0:
#             return d0

#         # Embed prompt once
#         p = self._embed_prompt(prompt)

#         # Layer 1: semantic noise
#         noise = max_sim(p, self.noise_anchors)
#         if noise > self.cfg.thresholds.layer1_noise_max_sim:
#             return Decision(
#                 "BLOCK",
#                 "semantic_noise",
#                 "This looks like non-work chatter. Please ask a work task (inventory/shipments/vendors/warehouse/forecasting).",
#                 similarity=noise,
#             )

#         # Layer 2: contrastive domain gate (pos vs neg + margin)
#         pos = max_sim(p, self.pos_anchors)
#         neg = max_sim(p, self.neg_anchors)
#         margin = pos - neg

#         if margin >= self.cfg.thresholds.layer2_margin_tau:
#             return Decision("ALLOW", "domain_match", "Allowed", similarity=pos, margin=margin)

#         return Decision(
#             "ROUTE",
#             "off_domain",
#             "This seems outside supply-chain scope. Rephrase with supply-chain context or route to a general assistant.",
#             similarity=pos,
#             margin=margin,
#         )
















        # Optional Layer 3: Mixed Intent Detection
    # def check(self, prompt: str) -> Decision:
    #     # Layer 0: cheap junk filter
    #     d0 = layer0_junk(prompt, self.cfg)
    #     if d0:
    #         return d0

    #     # Embed prompt once
    #     p = self._embed_prompt(prompt)

    #     # Layer 1: semantic noise (chitchat / non-work intent)
    #     noise = max_sim(p, self.noise_anchors)
    #     if noise > self.cfg.thresholds.layer1_noise_max_sim:
    #         # 👇 NEW: detect "mixed intent" (noise + domain together)
    #         pos = max_sim(p, self.pos_anchors)
    #         neg = max_sim(p, self.neg_anchors)
    #         margin = pos - neg

    #         if margin >= self.cfg.thresholds.layer2_margin_tau:
    #             return Decision(
    #                 "BLOCK",
    #                 "mixed_intent",
    #                 "Your prompt mixes non-work chatter with a supply-chain request. Please send only the work request (e.g., shipment tracking) without the joke/chitchat.",
    #                 similarity=noise,
    #                 margin=margin,
    #             )

    #         return Decision(
    #             "BLOCK",
    #             "semantic_noise",
    #             "This looks like non-work chatter. Please ask a work task (inventory/shipments/vendors/warehouse/forecasting).",
    #             similarity=noise,
    #         )

    #     # Layer 2: contrastive domain gate (pos vs neg + margin)
    #     pos = max_sim(p, self.pos_anchors)
    #     neg = max_sim(p, self.neg_anchors)
    #     margin = pos - neg

    #     if margin >= self.cfg.thresholds.layer2_margin_tau:
    #         return Decision("ALLOW", "domain_match", "Allowed", similarity=pos, margin=margin)

    #     return Decision(
    #         "ROUTE",
    #         "off_domain",
    #         "This seems outside supply-chain scope. Rephrase with supply-chain context or route to a general assistant.",
    #         similarity=pos,
    #         margin=margin,
    #     )









import re
import numpy as np
from dataclasses import dataclass
from .config import Config
from .similarity import max_sim, Embedder

# Simple keyword-based mixed-intent detector (enterprise-friendly)
# Keep this list small + obvious to avoid false positives.
_MIXED_INTENT_RE = re.compile(
    r"\b(joke|poem|trivia|funny|meme|story|song|riddle|who won|movie recommendation)\b",
    re.IGNORECASE
)

@dataclass
class Decision:
    decision: str  # ALLOW | BLOCK | ROUTE | REWRITE
    reason: str
    message: str
    similarity: float | None = None   # usually pos_sim for L2 allow/route OR noise_sim for L1 block
    margin: float | None = None
    approved_match: dict | None = None


def normalize(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t

def layer0_junk(prompt: str, cfg: Config) -> Decision | None:
    raw = prompt.strip()
    t = normalize(prompt)

    if not t:
        return Decision("BLOCK", "junk_empty", "Please share your work task (goal + context).")

    if t in set(cfg.layer0.junk_exact):
        return Decision("BLOCK", "junk_exact", "Please ask a work-related question with a goal + context.")

    if len(t.split()) < cfg.layer0.min_tokens:
        return Decision("BLOCK", "junk_too_short", "Please add more context (goal + details).")

    for pat in cfg.layer0.junk_regex:
        if re.match(pat, raw):
            return Decision("BLOCK", "junk_regex", "Please ask a work-related question with a goal + context.")

    return None

def is_mixed_intent(prompt: str) -> bool:
    return _MIXED_INTENT_RE.search(prompt or "") is not None

# class SentinelGate:
#     """
#     Config-driven hierarchical gate.
#     Uses injected Embedder so the model loads once and can be reused.
#     """
#     def __init__(self, cfg: Config, embedder: Embedder | None = None):
#         self.cfg = cfg
#         self.embedder = embedder or Embedder()

#         # Cache anchor embeddings once
#         self.noise_anchors = self.embedder.encode_list(cfg.layer1_noise_anchors)
#         self.pos_anchors = self.embedder.encode_list(cfg.layer2_domain_positive_anchors)
#         self.neg_anchors = self.embedder.encode_list(cfg.layer2_domain_negative_anchors)

#     def _embed_prompt(self, prompt: str) -> np.ndarray:
#         return self.embedder.encode_one(prompt)

#     def check(self, prompt: str) -> Decision:
#         # Layer 0: junk filter
#         d0 = layer0_junk(prompt, self.cfg)
#         if d0:
#             return d0

#         # Embed prompt once
#         p = self._embed_prompt(prompt)

#         # Layer 1: semantic noise (chitchat)
#         noise = max_sim(p, self.noise_anchors)
#         if noise > self.cfg.thresholds.layer1_noise_max_sim:
#             return Decision(
#                 "BLOCK",
#                 "semantic_noise",
#                 "This looks like non-work chatter. Please ask a work task (inventory/shipments/vendors/warehouse/forecasting).",
#                 similarity=noise,
#             )
        
#         # Layer 2: contrastive domain gate (pos vs neg + margin)
#         pos = max_sim(p, self.pos_anchors)
#         neg = max_sim(p, self.neg_anchors)
#         margin = pos - neg

#         # ✅ NEW: Mixed-intent guard (enterprise)
#         # If prompt contains obvious non-work request, block even if domain margin passes.
#         if margin >= self.cfg.thresholds.layer2_margin_tau and is_mixed_intent(prompt):
#             return Decision(
#                 "BLOCK",
#                 "mixed_intent",
#                 "Your prompt mixes non-work content (e.g., jokes) with a supply-chain request. Please send only the work request.",
#                 similarity=pos,
#                 margin=margin,
#             )
        
#         if margin >= self.cfg.thresholds.layer2_margin_tau:
#             return Decision("ALLOW", "domain_match", "Allowed", similarity=pos, margin=margin)

#         return Decision(
#             "ROUTE",
#             "off_domain",
#             "This seems outside supply-chain scope. Rephrase with supply-chain context or route to a general assistant.",
#             similarity=pos,
#             margin=margin,
#         )

class SentinelGate:
    """
    Config-driven hierarchical gate.
    Uses injected Embedder so the model loads once and can be reused.
    """
    def __init__(self, cfg: Config, embedder: Embedder | None = None, approved_store=None):
        self.cfg = cfg
        self.embedder = embedder or Embedder()

        # Cache anchor embeddings once
        self.noise_anchors = self.embedder.encode_list(cfg.layer1_noise_anchors)
        self.pos_anchors = self.embedder.encode_list(cfg.layer2_domain_positive_anchors)
        self.neg_anchors = self.embedder.encode_list(cfg.layer2_domain_negative_anchors)

        # ✅ Approved bypass store + in-memory index
        self.approved_store = approved_store
        self.approved_vecs = np.zeros((0, 384), dtype=np.float32)
        self.approved_meta: list[dict] = []  # keeps ids/domains/text aligned with vectors

        if self.approved_store is not None:
            self.refresh_approved()

    def refresh_approved(self) -> None:
        """
        Reload approved examples from JSON and rebuild in-memory vector index.
        Call this after admin approves a request (or on startup).
        """
        if self.approved_store is None:
            self.approved_vecs = np.zeros((0, 384), dtype=np.float32)
            self.approved_meta = []
            return

        rows = self.approved_store.list()  # list[ApprovedExample]
        if not rows:
            self.approved_vecs = np.zeros((0, 384), dtype=np.float32)
            self.approved_meta = []
            return

        self.approved_vecs = np.asarray([r.embedding for r in rows], dtype=np.float32)
        self.approved_meta = [{"id": r.id, "domain": r.domain, "text": r.text} for r in rows]

    def _embed_prompt(self, prompt: str) -> np.ndarray:
        return self.embedder.encode_one(prompt)

    def check(self, prompt: str) -> Decision:
        # Layer 0: junk filter
        d0 = layer0_junk(prompt, self.cfg)
        if d0:
            return d0

        # Embed prompt once
        p = self._embed_prompt(prompt)

        # Layer 1: semantic noise (chitchat)
        noise = max_sim(p, self.noise_anchors)
        if noise > self.cfg.thresholds.layer1_noise_max_sim:
            return Decision(
                "BLOCK",
                "semantic_noise",
                "This looks like non-work chatter. Please ask a work task (inventory/shipments/vendors/warehouse/forecasting).",
                similarity=noise,
            )

        # ✅ L2.5: approved bypass memory
        if self.approved_vecs.size > 0:
            sims = self.approved_vecs @ p  # dot-product (normalized)
            best_i = int(np.argmax(sims))
            best_sim = float(sims[best_i])

            if best_sim >= self.cfg.thresholds.approved_min_sim:
                meta = self.approved_meta[best_i] if best_i < len(self.approved_meta) else None
                return Decision(
                    "ALLOW",
                    "approved_match",
                    "Allowed (approved)",
                    similarity=best_sim,
                    margin=None,
                    approved_match={
                        "id": meta["id"],
                        "domain": meta["domain"],
                        "text": meta["text"],
                        "similarity": best_sim,
                    } if meta else {"similarity": best_sim},
                )
                # keep Decision simple; API can include meta if needed
                # return Decision("ALLOW", "approved_match", "Allowed (approved)", similarity=best_sim, margin=None)

        # Layer 2: contrastive domain gate (pos vs neg + margin)
        pos = max_sim(p, self.pos_anchors)
        neg = max_sim(p, self.neg_anchors)
        margin = pos - neg

        # Mixed-intent guard
        if margin >= self.cfg.thresholds.layer2_margin_tau and is_mixed_intent(prompt):
            return Decision(
                "BLOCK",
                "mixed_intent",
                "Your prompt mixes non-work content (e.g., jokes) with a supply-chain request. Please send only the work request.",
                similarity=pos,
                margin=margin,
            )

        if margin >= self.cfg.thresholds.layer2_margin_tau:
            return Decision("ALLOW", "domain_match", "Allowed", similarity=pos, margin=margin)

        return Decision(
            "ROUTE",
            "off_domain",
            "This seems outside supply-chain scope. Rephrase with supply-chain context or route to a general assistant.",
            similarity=pos,
            margin=margin,
        )
