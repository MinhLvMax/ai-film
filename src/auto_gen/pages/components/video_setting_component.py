
import re
from src.auto_gen.pages.components.base_component import BaseComponent
from src.auto_gen.pages.generation_config import VideoGenerationConfig
from src.auto_gen.constant import VideoModelNameString, RatiosMode, VideoGenerationMode
from playwright.sync_api import Page


class VideoSettingComponent(BaseComponent):
    def __init__(self, page):
        super().__init__(page)
        # Generation mode
        self.frames_mode = page.get_by_role("tab", name="crop_free Frames")
        self.ingrediens_mode = page.get_by_role("tab", name="chrome_extension Ingredients")

        # Ratios
        self.ratio_9_16 = page.get_by_role("tab", name="crop_9_16 9:")
        self.ratio_16_9 = page.get_by_role("tab", name="crop_16_9 16:")

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

        # Các nút chọn thời lượng
        self.dur_4s_btn = self.page.get_by_role("tab", name="4s")
        self.dur_6s_btn = self.page.get_by_role("tab", name="6s")
        self.dur_8s_btn = self.page.get_by_role("tab", name="8s")

    def _get_ratio_locator(self, ratio: RatiosMode):
        if ratio == RatiosMode.R_16_9:
            return self.ratio_16_9
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

    def _get_duration_locator(self, duration: int):
        if duration == 4:
            return self.dur_4s_btn
        if duration == 6:
            return self.dur_6s_btn
        if duration == 8:
            return self.dur_8s_btn

    def _get_video_generation_mode_locator(self, mode: VideoGenerationMode):
        if mode == VideoGenerationMode.FRAMES:
            return self.frames_mode
        elif mode == VideoGenerationMode.INGREDIENTS:
            return self.ingrediens_mode

    def configure(self, config: VideoGenerationConfig):
        # Tìm các nút
        generator_mode_locator = self._get_video_generation_mode_locator(config.generation_mode)
        ratio_locator = self._get_ratio_locator(config.ratio)
        quantity_locator = self._get_quantity_locator(config.quantity)
        dur_locator = self._get_duration_locator(config.duration)
        self.random_time_click(self.choose_model_btn)
        list_model = ListVideoModelComponent(self.page)
        model_locator = list_model.get_model_locator_by_name(config.model_name)
        self.random_time_click(model_locator)
        # Cho các locator vào danh sách rồi xáo trộn lên rồi click
        self.click_random_order(generator_mode_locator, ratio_locator, quantity_locator, dur_locator)
        self.close_component()


class ListVideoModelComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.omni = page.get_by_role("button", name="volume_up Omni Flash")
        self.veo31lite = page.get_by_role("button", name="volume_up Veo 3.1 - Lite", exact=True)
        self.veo31fast = page.get_by_role("button", name="volume_up Veo 3.1 - Fast")
        self.veo31qual = page.get_by_role("button", name="volume_up Veo 3.1 - Quality")
        self.veo31litelower = page.get_by_role("button", name="volume_up Veo 3.1 - Lite [")

    def get_model_locator_by_name(self, model_name):
        if model_name == VideoModelNameString.OMNI_FLASH:
            return self.omni
        elif model_name == VideoModelNameString.VEO_3_1_LITE:
            return self.veo31lite
        elif model_name == VideoModelNameString.VEO_3_1_FAST:
            return self.veo31fast
        elif model_name == VideoModelNameString.VEO_3_1_QUALITY:
            return self.veo31qual
        elif model_name == VideoModelNameString.VEO_3_1_LITE_LOWER_PRIORITY:
            return self.veo31litelower