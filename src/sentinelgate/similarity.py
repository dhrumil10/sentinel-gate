# import numpy as np

# def max_sim(vec: np.ndarray, anchors: np.ndarray) -> float:
#     """
#     vec: (D,)
#     anchors: (N, D) normalized embeddings
#     returns max cosine similarity
#     """
#     if anchors.size == 0:
#         return 0.0
#     denom = (np.linalg.norm(anchors, axis=1) * np.linalg.norm(vec) + 1e-12)
#     sims = (anchors @ vec) / denom
#     return float(np.max(sims))


# import numpy as np
# from sentence_transformers import SentenceTransformer

# class Embedder:
#     """
#     Single shared SentenceTransformer wrapper.
#     - Loads model once.
#     - Provides helpers to encode text(s) with normalized embeddings.
#     """
#     def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
#         self.model_name = model_name
#         self._model = SentenceTransformer(model_name)

#     def encode_list(self, texts: list[str]) -> np.ndarray:
#         if not texts:
#             return np.zeros((0, 384), dtype=np.float32)
#         embs = self._model.encode(texts, normalize_embeddings=True)
#         return np.asarray(embs, dtype=np.float32)

#     def encode_one(self, text: str) -> np.ndarray:
#         emb = self._model.encode([text], normalize_embeddings=True)[0]
#         return np.asarray(emb, dtype=np.float32)

# def max_sim(vec: np.ndarray, anchors: np.ndarray) -> float:
#     """
#     Assumes vec and anchors are already normalized (unit vectors),
#     so cosine similarity = dot product.
#     vec: (D,)
#     anchors: (N, D)
#     """
#     if anchors.size == 0:
#         return 0.0
#     sims = anchors @ vec
#     return float(np.max(sims))


import os
import logging
import numpy as np
from functools import lru_cache
from sentence_transformers import SentenceTransformer

# Enable debug logs by setting:
# PowerShell: $env:SENTINELGATE_DEBUG="1"
_DEBUG = os.getenv("SENTINELGATE_DEBUG", "").strip() in ("1", "true", "TRUE", "yes", "YES")

logger = logging.getLogger("sentinelgate")
if _DEBUG and not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


class Embedder:
    """
    Single shared SentenceTransformer wrapper.
    - Loads model once.
    - Optionally caches encode_one() results using LRU cache.
    """
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        enable_prompt_cache: bool = True,
        prompt_cache_maxsize: int = 2048,
    ):
        self.model_name = model_name
        self._model = SentenceTransformer(model_name)

        self._enable_prompt_cache = enable_prompt_cache
        self._prompt_cache_maxsize = prompt_cache_maxsize

        if _DEBUG:
            logger.info(f"[Embedder] Loaded model: {model_name}")
            logger.info(f"[Embedder] Prompt cache enabled={enable_prompt_cache} maxsize={prompt_cache_maxsize}")

        # Create a cached wrapper for encode_one if enabled
        if enable_prompt_cache:
            self._encode_one_cached = lru_cache(maxsize=prompt_cache_maxsize)(self._encode_one_uncached)
        else:
            self._encode_one_cached = None

    def encode_list(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, 384), dtype=np.float32)

        if _DEBUG:
            logger.info(f"[Embedder] Encoding anchor list: n={len(texts)}")

        embs = self._model.encode(texts, normalize_embeddings=True)
        return np.asarray(embs, dtype=np.float32)

    def _encode_one_uncached(self, text: str) -> tuple:
        # lru_cache needs hashable outputs, so we return a tuple then convert to np later
        if _DEBUG:
            logger.info(f"[Embedder] Encoding prompt (UNCACHED): {text[:80]!r}")

        emb = self._model.encode([text], normalize_embeddings=True)[0]
        return tuple(float(x) for x in emb)

    def encode_one(self, text: str) -> np.ndarray:
        if self._enable_prompt_cache:
            t = self._encode_one_cached(text)
            if _DEBUG:
                info = self._encode_one_cached.cache_info()
                logger.info(f"[Embedder] encode_one cache_info: hits={info.hits} misses={info.misses} currsize={info.currsize}")
            return np.asarray(t, dtype=np.float32)

        # no cache
        emb = self._model.encode([text], normalize_embeddings=True)[0]
        if _DEBUG:
            logger.info(f"[Embedder] Encoding prompt (NO CACHE): {text[:80]!r}")
        return np.asarray(emb, dtype=np.float32)

    def cache_info(self):
        if self._enable_prompt_cache and self._encode_one_cached:
            return self._encode_one_cached.cache_info()
        return None


def max_sim(vec: np.ndarray, anchors: np.ndarray) -> float:
    """
    Assumes vec and anchors are already normalized (unit vectors),
    so cosine similarity = dot product.
    vec: (D,)
    anchors: (N, D)
    """
    if anchors.size == 0:
        return 0.0
    sims = anchors @ vec
    return float(np.max(sims))
