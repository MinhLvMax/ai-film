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
        self.DONE_PROJECT_NAME = page.get_by_role("button", name="Done")

        # Entry nhập prompt
        # self.INPUT_PROMPT = page.get_by_role("paragraph").filter(has_text="What do you want to create?")
        self.INPUT_PROMPT = page.get_by_role("paragraph").filter(has_text=re.compile(r"^$"))
        # Nút cài đặt
        # self.SETTING = page.locator("button").filter(
        #     has_text=re.compile(r"(Nano Banana|Video)")
        # )
        self.SETTING = page.get_by_role("button", name="Settings trigger")

        # Nút gửi prompt tạo
        self.SEND_PROMPT = page.get_by_role("button", name="Start generation")

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
        # self.GENERATING_VIDEO = page.get_by_role(
        #     "link",
        #     name=re.compile(r"^play_circle\s*\d+%.*")
        # )
        self.GENERATING_VIDEO = page.get_by_text("%")

        # THông báo chung
        self.WARNING = page.get_by_text("warning")

        # Thông báo hành vi bất thường:
        self.UNUSUAL_ACTIVITY = page.get_by_role("button", name="warning Failed We noticed")

        # Thành phần setting
        self.setting_component = SettingComponent(self.page)

    async def turn_off_agent_mode(self):
        '''Tắt chế độ tác nhân'''
        if await self.AGENT.get_attribute("aria-pressed") == "true":
            await self.random_time_click(self.AGENT, msg='Tắt chế độ tác nhân')

    async def set_project_name(self, project_name: str):
        '''Đặt tên project theo tên được truyền vào'''
        await self.random_time_click(self.PROJECT_NAME, 'Đặt tên project')
        await self.PROJECT_NAME.fill(str(project_name))
        await self.random_time_click(self.DONE_PROJECT_NAME, 'Hoàn tất đặt tên')
        return True

    async def fill_and_send_prompt(self, prompt):
        '''Điền và gửi prompt, seting cần phải được cấu hình trước đó vì hàm này chỉ biết điền và gửi'''
        # print('Dừng để debug nút chỉnh sửa')
        # await self.page.pause()

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

    async def wait_until_creating_video_below(self, max_creating: int, poll_interval=5000):
        '''Chờ cho số lượng video đang được tạo giảm xuống dưới một ngưỡng nhất định'''
        while True:
            count = await self._creating_video_count()

            if count < max_creating:
                break

            print(f"{count=}")
            await self.page.wait_for_timeout(poll_interval)

        return True

    async def create_a_video(
            self,
            video_prompt: str,
            generation_mode: VideoGenerationMode,
            ratio: Ratio,
            quantity: Quantity,
            duration: Durations,
            model: VideoModels,
            max_creating: int,
            is_download: bool = False,
    ):
        '''Tạo độc lập 1 video từ 1 prompt truyền vào'''

        try:
            # await self.wait_until_creating_video_below(max_creating=max_creating)

            # await self.random_time_click(self.SETTING, 'Bật setting')
            await self.page.wait_for_load_state("animating_finished")  # Đợi các hiệu ứng kết thúc
            await self.SETTING.click(timeout=5000)

            await self.setting_component.configure_video(
                generation_mode, ratio, quantity, duration, model
            )

            # Lấy số lượng video đang được tạo trước khi chờ, phải tính từ trước khi gửi prompt
            # before_count = await self._creating_video_count()
            await self.fill_and_send_prompt(video_prompt)
            # is_video_registered = await self._wait_until_video_registered(before_count)

            # Nếu chế độ tải về đang bật thì tải phần tử gần nhất về

            return True
        except Exception as e:
            print(f'Có lỗi gì đó khiến tạo video thất bại {e}')
            return False

    async def _creating_video_count(self) -> int:
        '''Đếm số lượng video đang trong hàng đợi và đang được tạo'''
        print(f"QUEUE: {await self.QUEUED_VIDEO.all_inner_texts()}"[:50])
        print(f"GENERATE: {await self.GENERATING_VIDEO.all_inner_texts()}"[:50])
        return (
                await self.QUEUED_VIDEO.count()
                + await self.GENERATING_VIDEO.count()
        )

    async def _wait_until_video_registered(
            self,
            before_count,
            timeout: int = 30000,
            poll_interval: int = 1000,
    ):
        '''Đợi video vào trong hàng đợi'''
        elapsed = 0
        while elapsed < timeout:

            # Kiểm tra lỗi trước
            if await self.UNUSUAL_ACTIVITY.count() > 0:
                print("[ERROR] Unusual activity")
                return False

            # Kiểm tra video đã được hệ thống nhận chưa
            if await self._creating_video_count() > before_count:
                print("[OK] Video registered")
                return True

            await self.page.wait_for_timeout(poll_interval)
            elapsed += poll_interval
        raise TimeoutError("Video vừa gửi chưa xuất hiện trong queue/generating")

    async def _download_last_element(self, n_element):
        '''Thực hiện tải phần tử gần nhất mà vừa được tạo xong ở dạng 720 cho nhanh vì 1k 4k rất lâu'''
        print('Dừng để thiết kế logic tải n phần tử gần nhất về')
        await self.page.pause()

    async def check_notification(self):
        '''Kiểm tra xem có thông báo cảnh báo không'''
        if await self.WARNING.count() > 0:
            return True

        # if await self.SYSTEM_ALERT.count() > 0:
        #     return True
        #
        # if await self.MESSAGE.count() > 0:
        #     return True

        return False
