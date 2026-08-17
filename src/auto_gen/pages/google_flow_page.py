import re
from playwright.sync_api import Page
from src.auto_gen.pages.base_page import BasePage
from src.auto_gen.pages.google_flow_project_page import GoogleFlowProjectPage


class GoogleFlowPage(BasePage):
    url = 'https://labs.google/fx/tools/flow'

    def __init__(self, page: Page):
        super().__init__(page)
        self.go_to_this_page()
        self.create_with_google_flow_btn = page.get_by_role("button", name="Create with Google Flow")
        self.create_new_project_btn = page.get_by_role("button", name="add_2 New project")

    def create_with_google_flow(self):
        if self.create_with_google_flow_btn.is_visible():
            self.random_time_click(self.create_with_google_flow_btn)

    def _is_exist_project(self, project_name):
        return self.page.get_by_text(f"{project_name}editEdit project").is_visible()

    def _get_project_page(self):
        project_page = GoogleFlowProjectPage(self.page)
        project_page.wait_util_loaded()
        return project_page

    def _create_new_project(self, project_name):
        self.random_time_click(self.create_new_project_btn)
        new_project_page = self._get_project_page()
        new_project_page.set_project_name(project_name)
        return new_project_page

    def _open_exist_project_page(self, project_name):
        span = self.page.get_by_text(f"{project_name}editEdit project")
        a = span.locator("xpath=ancestor::div[2]/a")
        # self.debug_locator(a)
        # url_project = a.get_attribute("href")
        self.random_time_click(a)
        return self._get_project_page()

    def get_or_create_new_project(self, project_name):
        if self._is_exist_project(project_name):
            return self._open_exist_project_page(project_name)
        else:
            return self._create_new_project(project_name)





