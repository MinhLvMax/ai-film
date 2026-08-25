from playwright.async_api import async_playwright

from src.config import Config
from src.infrastructure.auto_sent_gg_flow.home_page import HomePage


class GoogleFlowSession:
    def __init__(self, user_profile=None, download_path=None):
        self.profile_path = user_profile or Config.BROWSER_PROFILES
        self.download_path = download_path or Config.BROWSER_DOWNLOAD_PATH

        self.playwright = None
        self.context = None
        self.page = None
        self.home_page = None

    async def start(self):
        self.playwright = await async_playwright().start()

        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_path,
            headless=False,
            channel="chrome",
            accept_downloads=True,
            downloads_path=self.download_path,
        )

        self.page = self.context.pages[0]

        self.home_page = HomePage(self.page)

        return self

    async def close_session(self):
        if self.context:
            await self.context.close()

        if self.playwright:
            await self.playwright.stop()
