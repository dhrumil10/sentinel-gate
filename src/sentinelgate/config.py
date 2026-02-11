from pydantic import BaseModel
from typing import List
import yaml

class Thresholds(BaseModel):
    layer1_noise_max_sim: float = 0.50
    layer2_margin_tau: float = 0.10
    approved_min_sim: float = 0.55

class Layer0Cfg(BaseModel):
    min_tokens: int = 2
    junk_exact: List[str] = []
    junk_regex: List[str] = []

class Config(BaseModel):
    domain: str = "supply_chain"
    thresholds: Thresholds = Thresholds()
    layer0: Layer0Cfg = Layer0Cfg()
    layer1_noise_anchors: List[str] = []
    layer2_domain_positive_anchors: List[str] = []
    layer2_domain_negative_anchors: List[str] = []

def load_config(path: str = "config.yaml") -> Config:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return Config(**data)

