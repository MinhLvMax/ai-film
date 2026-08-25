from playwright.async_api import Page
from src.infrastructure.auto_sent_gg_flow.base_page import BasePage
from src.domain import VideoModels


class ListVideoModelComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.OMNI = page.get_by_role("button", name="volume_up Omni Flash")
        self.VEO_31_LITE = page.get_by_role("button", name="volume_up Veo 3.1 - Lite", exact=True)
        self.VEO_31_FAST = page.get_by_role("button", name="volume_up Veo 3.1 - Fast")
        self.VEO_31_QUALITY = page.get_by_role("button", name="volume_up Veo 3.1 - Quality")
        self.VEO_31_LITE_LOWER_PRIORITY = page.get_by_role("button", name="volume_up Veo 3.1 - Lite [")

    def get_model_locator_by_name(
            self,
            model_name: VideoModels
    ):
        """Lấy locator model theo tên truyền vào."""
        locators = {
            VideoModels.OMNI_FLASH: self.OMNI,
            VideoModels.VEO_31_LITE: self.VEO_31_LITE,
            VideoModels.VEO_31_FAST: self.VEO_31_FAST,
            VideoModels.VEO_31_QUALITY: self.VEO_31_QUALITY,
            VideoModels.VEO_31_LOWER_PRIORITY: self.VEO_31_LITE_LOWER_PRIORITY,
        }
        return locators[model_name]
