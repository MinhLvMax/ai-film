from enum import StrEnum, IntEnum


class ImageModel(StrEnum):
    NANO_BANANA_PRO = "Nano Banana Pro"
    NANO_BANANA_2 = "Nano Banana 2"
    NANO_BANANA_2_LITE = "Nano Banana 2 Lite"


class VideoModels(StrEnum):
    OMNI_FLASH = "Omni Flash"
    VEO_31_LITE = "Veo 3.1 - Lite"
    VEO_31_FAST = "Veo 3.1 - Fast"
    VEO_31_QUALITY = "Veo 3.1 - Quality"
    VEO_31_LOWER_PRIORITY = "Veo 3.1 - Lower Priority"


class Ratio(StrEnum):
    RATIO_16_9 = "16:9"
    RATIO_4_3 = "4:3"
    RATIO_1_1 = "1:1"
    RATIO_3_4 = "3:4"
    RATIO_9_16 = "9:16"


class Quantity(IntEnum):
    X1 = 1
    X2 = 2
    X3 = 3
    X4 = 4


class VideoGenerationMode(StrEnum):
    FRAMES = "Frames"
    INGREDIENTS = "Ingredients"


class Durations(StrEnum):
    DURATION_4S = '4s'
    DURATION_6S = '6s'
    DURATION_8S = '8s'
    DURATION_10S = '10s'
