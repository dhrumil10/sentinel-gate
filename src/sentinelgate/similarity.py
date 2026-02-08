import numpy as np

def max_sim(vec: np.ndarray, anchors: np.ndarray) -> float:
    """
    vec: (D,)
    anchors: (N, D) normalized embeddings
    returns max cosine similarity
    """
    if anchors.size == 0:
        return 0.0
    denom = (np.linalg.norm(anchors, axis=1) * np.linalg.norm(vec) + 1e-12)
    sims = (anchors @ vec) / denom
    return float(np.max(sims))
