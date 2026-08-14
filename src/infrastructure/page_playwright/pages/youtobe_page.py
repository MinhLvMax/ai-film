from playwright.sync_api import Page
from src.infrastructure.page_playwright.pages.base_page import BasePage


class YoutobePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)


if __name__ == '__main__':
    from src.infrastructure.page_playwright.context import ContextFactory

    ctx = ContextFactory()
