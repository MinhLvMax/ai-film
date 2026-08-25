import re
from playwright.async_api import Page
from src.infrastructure.auto_sent_gg_flow.base_page import BasePage
from src.infrastructure.auto_sent_gg_flow.home_page.project_page.setting_component import \
    SettingComponent
from src.domain import VideoGenerationMode, Ratio, Quantity, Durations, VideoModels


class ProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.ALL_MEDIA = page.get_by_role("button", name="dashboard All Media")
        self.IMAGES = page.get_by_role("button", name="image View images")
        self.VIDEOS = page.get_by_role("button", name="videocam View videos")
        self.CHARACTERS = page.get_by_role("button", name="accessibility_new Characters")
        self.SCENES = page.get_by_role("button", name="movie View scenes")
        # Nút thêm thành phần tham chiếu
        self.ADD_REFERENCE = page.get_by_role("button", name="add_2 Create")
        # Nút chế độ tác nhân
        self.AGENT = page.get_by_role("button", name="Agent")
        # Entry tên project
        self.PROJECT_NAME = page.get_by_role("textbox", name="Editable text")
        # Nút hoàn tất đặt tên
        self.DONE_PROJECT_NAME = page.get_by_role("button", name="done Done")
        # Entry nhập prompt
        self.INPUT_PROMPT = page.get_by_role("paragraph").filter(has_text="What do you want to create?")
        # Nút cài đặt
        self.SETTING = page.locator("button").filter(
            has_text=re.compile(r"(Nano Banana|Video)")
        )
        # Nút gửi prompt tạo
        self.SEND_PROMPT = page.get_by_role("button", name="arrow_forward Create")
        # Ảnh đang được tạo
        self.CREATING_IMAGES = self.page.get_by_text(
            re.compile(r"image\d+%.*")
        )
        # Video đang trong hàng đợi
        self.QUEUED_VIDEO = page.get_by_role(
            "button",
            name=re.compile(r"^movie\s+Queued.*")
        )
        # Video đang được Generate
        self.GENERATING_VIDEO = page.get_by_role(
            "link",
            name=re.compile(r"^play_circle\s+\d+%.*")
        )

        # Thành phần setting
        self.setting_component = SettingComponent(self.page)

    async def turn_off_agent_mode(self):
        '''Tắt chế độ tác nhân'''
        if self.AGENT.get_attribute("aria-pressed") == "true":
            await self.random_time_click(self.AGENT, msg='Tắt chế độ tác nhân')

    async def set_project_name(self, project_name: str):
        '''Đặt tên project theo tên được truyền vào'''
        await self.random_time_click(self.PROJECT_NAME, 'Đặt tên project')
        await self.PROJECT_NAME.fill(project_name)
        await self.random_time_click(self.DONE_PROJECT_NAME, 'Hoàn tất đặt tên')
        return True

    async def fill_and_send_prompt(self, prompt):
        '''Điền và gửi prompt, seting cần phải được cấu hình trước đó vì hàm này chỉ biết điền và gửi'''
        await self.INPUT_PROMPT.fill(prompt)
        await self.random_time_click(self.SEND_PROMPT, 'Gửi prompt')
        return True

    async def wait_until_creating_image_below(
            self,
            max_creating: int = 2,
            poll_interval: int = 5000,
    ):
        '''Chờ cho số lượng ảnh đang được tạo giảm xuống dưới một ngưỡng nhất định'''
        while await self.CREATING_IMAGES.count() >= max_creating:
            print(f'{self.CREATING_IMAGES.count()=}')
            await self.page.wait_for_timeout(poll_interval)

    def wait_until_creating_video_below(self, max_creating: int = 2, poll_interval=5000):
        '''Chờ cho số lượng video đang được tạo giảm xuống dưới một ngưỡng nhất định'''
        while self._creating_video_count() >= max_creating:
            print(f'{self._creating_video_count()=}')
            self.page.wait_for_timeout(poll_interval)
        return True

    async def create_a_video(self,
                             video_prompt: str,
                             generation_mode: VideoGenerationMode,
                             ratio: Ratio,
                             quantity: Quantity,
                             duration: Durations,
                             model: VideoModels):
        '''Tạo độc lập 1 video từ 1 prompt truyền vào'''
        await self.random_time_click(self.SETTING, 'Bật setting')
        await self.setting_component.configure_video(
            generation_mode, ratio, quantity, duration, model
        )
        await self.fill_and_send_prompt(video_prompt)

    async def _creating_video_count(self) -> int:
        '''Đếm số lượng video đang trong hàng đợi và đang được tạo'''
        print("QUEUE:", self.QUEUED_VIDEO.all_inner_texts())
        print("GENERATE:", self.GENERATING_VIDEO.all_inner_texts())
        return (
                await self.QUEUED_VIDEO.count()
                + await self.GENERATING_VIDEO.count()
        )
