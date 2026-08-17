from dataclasses import dataclass
from .base_generation_config import BaseGenerationConfig
from src.auto_gen.constant.image_models_name import ImageModelNameString
@dataclass
class ImageGenerationConfig(BaseGenerationConfig):
    model_name: str = ImageModelNameString.Nano_Banana_2
