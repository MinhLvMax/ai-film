from playwright.sync_api import Page
from src.infrastructure.auto_send_prompts.google_flow.base_page import BasePage


class Home(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.URL = 'https://labs.google/fx/tools/flow'

        self.CREATE_WITH_GG_FLOW = page.get_by_role("button", name="Create with Google Flow")
        self.NEW_PROJECT = page.get_by_role("button", name="add_2 New project")

    def go(self):
        self.page.goto(self.URL)
