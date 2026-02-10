
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

class SentinelGate:
    """
    Config-driven hierarchical gate.
    Uses injected Embedder so the model loads once and can be reused.
    """
    def __init__(self, cfg: Config, embedder: Embedder | None = None):
        self.cfg = cfg
        self.embedder = embedder or Embedder()

        # Cache anchor embeddings once
        self.noise_anchors = self.embedder.encode_list(cfg.layer1_noise_anchors)
        self.pos_anchors = self.embedder.encode_list(cfg.layer2_domain_positive_anchors)
        self.neg_anchors = self.embedder.encode_list(cfg.layer2_domain_negative_anchors)

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

        # Layer 2: contrastive domain gate (pos vs neg + margin)
        pos = max_sim(p, self.pos_anchors)
        neg = max_sim(p, self.neg_anchors)
        margin = pos - neg

        # ✅ NEW: Mixed-intent guard (enterprise)
        # If prompt contains obvious non-work request, block even if domain margin passes.
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
