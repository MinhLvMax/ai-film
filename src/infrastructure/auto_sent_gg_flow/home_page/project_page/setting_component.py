from playwright.async_api import Page
from src.infrastructure.auto_sent_gg_flow.base_page import BasePage
from src.infrastructure.auto_sent_gg_flow.home_page.project_page.image_setting_component import \
    ImageSettingComponent
from src.infrastructure.auto_sent_gg_flow.home_page.project_page.video_setting_component import \
    VideoSettingComponent


class SettingComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Nút tab ảnh
        self.IMAGE_TAB = page.get_by_role("radio", name="Image")

        # Nút tab video
        self.VIDEO_TAB = page.get_by_role("radio", name="Video")

        # Thành phần bên trong
        self._image_setting_component = ImageSettingComponent(self.page)
        self._video_setting_component = VideoSettingComponent(self.page)

    async def configure_image(self, ratio, quantity, model):
        '''Bật tab image và cấu hình theo tham số'''
        await self.random_time_click(self.IMAGE_TAB, 'Tab ảnh trong setting')

        await self._image_setting_component.configure(
            ratio=ratio,
            quantity=quantity,
            model=model,
        )

    async def configure_video(self, generation_mode, ratio, quantity, duration, model):
        '''Bật tab video và cấu hình theo tham số'''
        await self.random_time_click(self.VIDEO_TAB, 'Tab video trong setting')

        await self._video_setting_component.configure(
            generation_mode=generation_mode,
            ratio=ratio,
            quantity=quantity,
            duration=duration,
            model=model,
        )
