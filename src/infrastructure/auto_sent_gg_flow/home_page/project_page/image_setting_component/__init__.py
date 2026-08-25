import re
from playwright.async_api import Page
from src.infrastructure.auto_sent_gg_flow.base_page import BasePage
from src.infrastructure.auto_sent_gg_flow.home_page.project_page.image_setting_component.list_image_model_component import \
    ListImageModelComponent
from src.domain import Ratio, Quantity, ImageModel


class ImageSettingComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Các nút chọn tỷ lệ
        self.RATIO_16_9 = self.page.get_by_role("tab", name="crop_16_9 16:")
        self.RATIO_4_3 = self.page.get_by_role("tab", name="crop_landscape 4:")
        self.RATIO_1_1 = self.page.get_by_role("tab", name="crop_square 1:")
        self.RATIO_1_2 = self.page.get_by_role("tab", name="crop_square 1:")
        self.RATIO_3_4 = self.page.get_by_role("tab", name="crop_portrait 3:")
        self.RATIO_9_16 = self.page.get_by_role("tab", name="crop_9_16 9:")

        # Các nút chọn số lượng
        self.QUANTITY_X1 = self.page.get_by_role("tab", name="x1")
        self.QUANTITY_X2 = self.page.get_by_role("tab", name="x2")
        self.QUANTITY_X3 = self.page.get_by_role("tab", name="x3")
        self.QUANTITY_X4 = self.page.get_by_role("tab", name="x4")

        # Nút chọn model
        self.CHOOSE_MODEL = self.page.get_by_role(
            "button",
            name=re.compile(r"arrow_drop_down$")
        )

        self.list_model_component = ListImageModelComponent(self.page)

    async def configure(self,
                  ratio: Ratio,
                  quantity: Quantity,
                  model: ImageModel):
        '''Cấu hình setting theo tham số truyền vào'''

        # Tìm các nút
        ratio_locator = self._get_ratio_locator(ratio)
        quantity_locator = self._get_quantity_locator(quantity)
        self.random_time_click(self.CHOOSE_MODEL, 'Mở list model tạo ảnh')
        model_locator = self.list_model_component.get_model_locator_by_name(model)
        self.random_time_click(model_locator, f'Chọn model {model}')
        # Cho các locator vào danh sách rồi xáo trộn lên rồi click
        self.click_random_order(ratio_locator, quantity_locator)
        self.close_component()

    def _get_ratio_locator(self, ratio: Ratio):
        locators = {
            Ratio.RATIO_16_9: self.RATIO_16_9,
            Ratio.RATIO_4_3: self.RATIO_4_3,
            Ratio.RATIO_1_1: self.RATIO_1_1,
            Ratio.RATIO_3_4: self.RATIO_3_4,
            Ratio.RATIO_9_16: self.RATIO_9_16,
        }
        return locators[ratio]

    def _get_quantity_locator(self, quantity: Quantity):
        locators = {
            Quantity.X1: self.QUANTITY_X1,
            Quantity.X2: self.QUANTITY_X2,
            Quantity.X3: self.QUANTITY_X3,
            Quantity.X4: self.QUANTITY_X4,
        }
        return locators[quantity]
