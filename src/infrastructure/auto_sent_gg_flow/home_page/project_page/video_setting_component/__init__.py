import re
from playwright.async_api import Page
from src.infrastructure.auto_sent_gg_flow.base_page import BasePage
from src.infrastructure.auto_sent_gg_flow.home_page.project_page.video_setting_component.list_video_model_component import \
    ListVideoModelComponent
from src.domain import VideoGenerationMode, Ratio, Quantity, Durations, VideoModels


class VideoSettingComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Generation mode
        self.FRAME_MODE = page.get_by_role("tab", name="crop_free Frames")
        self.INGREDIENS_MODE = page.get_by_role("tab", name="chrome_extension Ingredients")

        # Ratios
        self.RATIO_9_16 = page.get_by_role("tab", name="crop_9_16 9:")
        self.RATIO_16_9 = page.get_by_role("tab", name="crop_16_9 16:")

        # Các nút chọn số lượng
        self.QUANTIRY_X1 = self.page.get_by_role("tab", name="x1")
        self.QUANTIRY_X2 = self.page.get_by_role("tab", name="x2")
        self.QUANTITY_X3 = self.page.get_by_role("tab", name="x3")
        self.QUANTIRY_X4 = self.page.get_by_role("tab", name="x4")

        # Nút chọn model
        self.CHOOSE_VIDEO_MODEL = self.page.get_by_role(
            "button",
            name=re.compile(r"arrow_drop_down$")
        )

        # Các nút chọn thời lượng
        self.DUR_4S = self.page.get_by_role("tab", name="4s")
        self.DUR_6S = self.page.get_by_role("tab", name="6s")
        self.DUR_8S = self.page.get_by_role("tab", name="8s")
        self.DUR_10S = self.page.get_by_role("tab", name="10s")

        self.list_video_model_component = ListVideoModelComponent(self.page)

    async def configure(self,
                  generation_mode: VideoGenerationMode,
                  ratio: Ratio,
                  quantity: Quantity,
                  duration: Durations,
                  model: VideoModels,
                  ):
        '''cấu hình setting video theo tham số truyền vào'''
        # Tìm các nút
        generator_mode_locator = self._get_video_generation_mode_locator(generation_mode)
        ratio_locator = self._get_ratio_locator(ratio)
        quantity_locator = self._get_quantity_locator(quantity)
        dur_locator = self._get_duration_locator(duration)
        self.random_time_click(self.CHOOSE_VIDEO_MODEL, 'Mở list video model')
        model_locator = self.list_video_model_component.get_model_locator_by_name(model)
        self.random_time_click(model_locator, f'Chọn model {model}')
        # Cho các locator vào danh sách rồi xáo trộn lên rồi click
        self.click_random_order(generator_mode_locator, ratio_locator, quantity_locator, dur_locator)
        self.close_component()

    def _get_ratio_locator(self, ratio: Ratio):
        '''Lấy nút ratio theo tên truyền vào'''
        locators = {
            Ratio.RATIO_16_9: self.RATIO_16_9,
            Ratio.RATIO_9_16: self.RATIO_9_16,
        }

        return locators[ratio]

    def _get_quantity_locator(self, quantity: Quantity):
        '''Lấy nút chất lượng theo tên truyền vào'''
        locators = {
            Quantity.X1: self.QUANTIRY_X1,
            Quantity.X2: self.QUANTIRY_X2,
            Quantity.X3: self.QUANTITY_X3,
            Quantity.X4: self.QUANTIRY_X4,
        }

        return locators[quantity]

    def _get_duration_locator(self, duration: Durations):
        """Lấy nút thời gian theo giá trị truyền vào."""
        locators = {
            Durations.DURATION_4S: self.DUR_4S,
            Durations.DURATION_6S: self.DUR_6S,
            Durations.DURATION_8S: self.DUR_8S,
            Durations.DURATION_10S: self.DUR_10S,
        }

        return locators[duration]

    def _get_video_generation_mode_locator(
            self,
            mode: VideoGenerationMode
    ):
        """Lấy nút chế độ tạo video theo tên truyền vào."""
        locators = {
            VideoGenerationMode.FRAMES: self.FRAME_MODE,
            VideoGenerationMode.INGREDIENTS: self.INGREDIENS_MODE,
        }

        return locators[mode]
