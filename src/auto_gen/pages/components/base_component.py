from playwright.sync_api import Page
from src.auto_gen.pages.base_page import BasePage

class BaseComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    def close_component(self):
        self.page.keyboard.press('Escape')
