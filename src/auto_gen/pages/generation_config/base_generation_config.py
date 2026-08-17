from dataclasses import dataclass
from src.auto_gen.constant import RatiosMode

@dataclass
class BaseGenerationConfig:
    quantity: int = 1
    ratio: RatiosMode = RatiosMode.R_16_9