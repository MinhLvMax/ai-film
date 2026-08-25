from playwright.async_api import Page
from src.infrastructure.auto_sent_gg_flow.base_page import BasePage
from src.domain import ImageModel


class ListImageModelComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.NANO_PRO = page.get_by_role("button", name="🍌 Nano Banana Pro")
        self.NANO_2 = page.get_by_role("button", name="🍌 Nano Banana 2", exact=True)
        self.NANO_2_LITE = page.get_by_role("button", name="🍌 Nano Banana 2 Lite")

    def get_model_locator_by_name(
            self,
            model_name: ImageModel
    ):
        """Lấy locator model theo tên truyền vào."""
        locators = {
            ImageModel.NANO_BANANA_PRO: self.NANO_PRO,
            ImageModel.NANO_BANANA_2: self.NANO_2,
            ImageModel.NANO_BANANA_2_LITE: self.NANO_2_LITE,
        }

        return locators[model_name]
