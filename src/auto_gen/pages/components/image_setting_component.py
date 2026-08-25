import re
import random
from playwright.sync_api import Page
from src.auto_gen.pages.components.base_component import BaseComponent
from src.auto_gen.constant import ImageModelNameString, RatiosMode
from src.auto_gen.pages.generation_config import ImageGenerationConfig


class ImageSettingComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        # Các nút chọn tỷ lệ
        self.ratio_16_9 = self.page.get_by_role("tab", name="crop_16_9 16:")
        self.ratio_4_3 = self.page.get_by_role("tab", name="crop_landscape 4:")
        self.ratio_1_1 = self.page.get_by_role("tab", name="crop_square 1:")
        self.ratio_1_2 = self.page.get_by_role("tab", name="crop_square 1:")
        self.ratio_3_4 = self.page.get_by_role("tab", name="crop_portrait 3:")
        self.ratio_9_16 = self.page.get_by_role("tab", name="crop_9_16 9:")

        # Các nút chọn số lượng
        self.quantity_x1 = self.page.get_by_role("tab", name="x1")
        self.quantity_x2 = self.page.get_by_role("tab", name="x2")
        self.quantity_x3 = self.page.get_by_role("tab", name="x3")
        self.quantity_x4 = self.page.get_by_role("tab", name="x4")

        # Nút chọn model
        self.choose_model_btn = self.page.get_by_role(
            "button",
            name=re.compile(r"arrow_drop_down$")
        )

    def _get_ratio_locator(self, ratio: RatiosMode):
        if ratio == RatiosMode.R_16_9:
            return self.ratio_16_9
        if ratio == RatiosMode.R_4_3:
            return self.ratio_4_3
        if ratio == RatiosMode.R_1_1:
            return self.ratio_1_1
        if ratio == RatiosMode.R_3_4:
            return self.ratio_3_4
        if ratio == RatiosMode.R_9_16:
            return self.ratio_9_16

    def _get_quantity_locator(self, quantity: int):
        if quantity == 1:
            return self.quantity_x1
        if quantity == 2:
            return self.quantity_x2
        if quantity == 3:
            return self.quantity_x3
        if quantity == 4:
            return self.quantity_x4

    def configure(self, config: ImageGenerationConfig):
        # Tìm các nút
        ratio_locator = self._get_ratio_locator(config.ratio)
        quantity_locator = self._get_quantity_locator(config.quantity)
        self.random_time_click(self.choose_model_btn)
        list_model = ListImageModelComponent(self.page)
        model_locator = list_model.get_model_locator_by_name(config.model_name)
        self.random_time_click(model_locator)
        # Cho các locator vào danh sách rồi xáo trộn lên rồi click
        locators = [
            ratio_locator,
            quantity_locator,
        ]
        random.shuffle(locators)
        for locator in locators:
            self.random_time_click(locator)
        self.close_component()


class ListImageModelComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.nano_pro = page.get_by_role("button", name="🍌 Nano Banana Pro")
        self.nano_2 = page.get_by_role("button", name="🍌 Nano Banana 2", exact=True)
        self.nano_2_lite = page.get_by_role("button", name="🍌 Nano Banana 2 Lite")

    def get_model_locator_by_name(self, model_name):
        if model_name == ImageModelNameString.Nano_Banana_pro:
            return self.nano_pro
        if model_name == ImageModelNameString.Nano_Banana_2:
            return self.nano_2
        if model_name == ImageModelNameString.Nano_Banana_2_lite:
            return self.nano_2_lite
