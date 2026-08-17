import re
import time
from src.auto_gen.constant.resoluion import Resolution
from src.auto_gen.constant import RatiosMode, ImageModelNameString, VideoGenerationMode, VideoModelNameString, GenMode
from .base_page import BasePage
from .generation_config import BaseGenerationConfig, ImageGenerationConfig, VideoGenerationConfig
from playwright.sync_api import Page
from src.auto_gen.pages.components.setting_component import SettingComponent
from src.auto_gen.pages.components.add_reference_component import AddReferenceComponent
from src.auto_gen.pages.components.right_click_menu_component import RightClickMenuComponent


class GoogleFlowProjectPage(BasePage):
    '''
    Đây là page khi mà mở vào trong một project
    '''
    url = None

    def __init__(self, page: Page):
        super().__init__(page)
        # entry tên project
        self.name_entry = page.get_by_role("textbox", name="Editable text")
        # nút hoàn tất đặt tên
        self.done_project_name_btn = page.get_by_role("button", name="done Done")
        # mục tất cả media
        self.all_media_btn = page.get_by_text("dashboardAll MediaAll Media")
        # thông báo hoạt động bất thường
        self.unusual_activity_notice = page.get_by_role("button", name="warning Failed We noticed")
        # mục chỉ ảnh
        self.images = page.get_by_text("imageView imagesImages")
        # mục chỉ video
        self.videos = page.get_by_text("videocamView videosVideos")
        # entry nhập prompt
        self.input_prompt = page.get_by_role("paragraph").filter(has_text="What do you want to create?")
        # nút chế độ tác nhân
        self.agent_btn = page.get_by_role("button", name="Tác nhân")
        # nút thêm thành phần tham chiếu
        self.add_image = page.get_by_role("button", name="add_2 Create")
        # nút cài đặt
        self.setting_btn = page.locator("button").filter(
            has_text=re.compile(r"(Nano Banana|Video)")
        )
        # nút gửi prompt tạo
        self.send_btn = page.get_by_role("button", name="arrow_forward Create")

        # ảnh đang được tạo
        self.creating_images = self.page.get_by_text(
            re.compile(r"image\d+%.*")
        )

        # Các locator nhận diện video đang tạo
        # # 1. Vừa submit, chưa có Queue, chưa có %
        # self.submitting_video = page.get_by_text(
        #     re.compile(r"^play_circle(?!\s+\d+%).*")
        # )

        # 2. Đang Queue
        self.queued_video = page.get_by_role(
            "button",
            name=re.compile(r"^movie\s+Queued.*")
        )

        # 3. Đang Generate
        self.generating_video = page.get_by_role(
            "link",
            name=re.compile(r"^play_circle\s+\d+%.*")
        )

    def turn_off_agent_btn(self):
        pressed = self.agent_btn.get_attribute("aria-pressed")
        if pressed == 'true':
            print('Tắt chế độ tác nhân')
            self.random_time_click(self.agent_btn)
        return True

    def set_project_name(self, project_name: str):
        self.random_time_click(self.name_entry)
        self.name_entry.fill(project_name)
        self.random_time_click(self.done_project_name_btn)
        return True

    def _go_to_setting(self):
        self.click_random_order(self.setting_btn)
        print('Mở cửa sổ cài đặt')
        return SettingComponent(self.page)

    def fill_prompt(self, prompt):
        self.input_prompt.fill(prompt)
        return True

    def turn_on_image_mode(self, config: ImageGenerationConfig):
        setting_component = self._go_to_setting()
        image_setting_component = setting_component.go_to_image_mode()
        image_setting_component.configure(config)
        return True

    def turn_on_video_mode(self, config: VideoGenerationConfig):
        setting_component = self._go_to_setting()
        video_setting_component = setting_component.go_to_video_mode()
        video_setting_component.configure(config)
        return True

    def send_a_prompt(self, prompt: str, mode: GenMode, config):
        self.fill_prompt(prompt)
        if mode == GenMode.IMAGE:
            self.turn_on_image_mode(config)
        if mode == GenMode.VIDEO:
            self.turn_on_video_mode(config)
        self.random_time_click(self.send_btn)

    def wait_until_creating_image_below(
            self,
            max_creating: int = 2,
            timeout: int = 60_000,
            poll_interval: int = 5000,
    ):
        start = time.time()
        while self.creating_images.count() >= max_creating:
            print(f'{self.creating_images.count()=}')
            if (time.time() - start) * 1000 > timeout:
                raise TimeoutError(
                    f"Still have {self.creating_images.count()} creating images after {timeout} ms"
                )
            self.page.wait_for_timeout(poll_interval)

    def _creating_video_count(self) -> int:
        # print("SUBMIT:", self.submitting_video.all_inner_texts())
        print("QUEUE:", self.queued_video.all_inner_texts())
        print("GENERATE:", self.generating_video.all_inner_texts())
        return (
            # self.submitting_video.count()
                + self.queued_video.count()
                + self.generating_video.count()
        )

    def wait_until_creating_video_below(self, max_creating: int = 2, timeout=120_000, poll_interval=5000):
        start = time.time()
        while self._creating_video_count() >= max_creating:
            print(f'{self._creating_video_count()=}')
            if (time.time() - start) * 1000 > timeout:
                raise TimeoutError(
                    f"Still have {self._creating_video_count()} creating images after {timeout} ms"
                )
            self.page.wait_for_timeout(poll_interval)
        return True

    def _get_lasted_img(self, config):
        self.turn_on_video_mode(config)
        self.random_time_click(self.add_image)
        add_ref_com_obj = AddReferenceComponent(self.page)
        add_ref_com_obj.add_latest_image()
        return True

    def create_video_from_latest_image(self, prompt, config: VideoGenerationConfig):
        self._get_lasted_img(config)
        self.send_a_prompt(prompt, GenMode.VIDEO, config)
        if config.resolution:
            self.download_lasted_video(config.resolution)
        return True

    def download_lasted_video(self, resolution: Resolution):
        self.random_time_click(self.videos)
        lasted_video_locator = self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).first
        lasted_video_locator.hover()
        lasted_video_locator.click(button='right')
        right_click_menu = RightClickMenuComponent(self.page)
        right_click_menu.download_this_video(resolution)
        return
