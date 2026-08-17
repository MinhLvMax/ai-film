from enum import Enum


class VideoModelNameString(str, Enum):
    OMNI_FLASH = "Omni Flash"
    VEO_3_1_LITE = 'Veo 3.1 - Lite'
    VEO_3_1_FAST = 'Veo 3.1 - Fast'
    VEO_3_1_QUALITY = 'Veo 3.1 - Quality'
    VEO_3_1_LITE_LOWER_PRIORITY = 'Veo 3.1 - Lower Priority'

