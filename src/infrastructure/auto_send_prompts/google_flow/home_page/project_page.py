from playwright.sync_api import Page
import re
from src.infrastructure.auto_send_prompts.helper import random_time_click
from src.infrastructure.auto_send_prompts.google_flow.base_page import BasePage


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

    def turn_off_agent_mode(self):
        '''Tắt chế độ tác nhân'''
        if self.AGENT.get_attribute("aria-pressed") == "true":
            random_time_click(self.AGENT, message='Click nút random')

    def set_project_name(self, project_name: str):
        '''Đặt tên project theo tên được truyền vào'''
        random_time_click(self.PROJECT_NAME, message='Click nút ')
        self.PROJECT_NAME.click()
        self.PROJECT_NAME.fill(project_name)
        random_time_click(self.DONE_PROJECT_NAME)
        return True
