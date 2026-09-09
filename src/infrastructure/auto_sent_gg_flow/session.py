import subprocess
from typing import Literal
from playwright.async_api import async_playwright, Page
from src.config import Config
from src.infrastructure.auto_sent_gg_flow.home_page import HomePage

BrowserName = Literal[
    "chrome",
    "chrome-beta",
    "chrome-dev",
    "chrome-canary",

    "msedge",
    "msedge-beta",
    "msedge-dev",
    "msedge-canary",

    "coc_coc",
    "opera",

    "firefox",
]


class GoogleFlowSession:
    CDP_HOST = "127.0.0.1"
    CDP_PORT = 9222

    def __init__(
            self,
            user_profile=None,
            download_path=None,
            browser_name: BrowserName | None = None,
            executable_path: str | None = None,
    ):
        self.profile_path = user_profile or Config.BROWSER_PROFILES
        self.download_path = download_path or Config.BROWSER_DOWNLOAD_PATH

        self.playwright = None
        self.browser_name = browser_name or 'chrome'
        self.context = None
        self.page: Page | None = None
        self.home_page = None

        self.chrome_process = None
        self.executable_path = executable_path

    async def start(self):
        self.playwright = await async_playwright().start()

        if self.browser_name == "firefox":
            self.context = await self.playwright.firefox.launch_persistent_context(
                user_data_dir=self.profile_path,
                headless=False,
                accept_downloads=True,
                downloads_path=self.download_path,
            )

        elif self.browser_name == "coc_coc":
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.profile_path,
                headless=False,
                executable_path=self.executable_path,
                accept_downloads=True,
                downloads_path=self.download_path,
            )

        elif self.browser_name == "opera":
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.profile_path,
                headless=False,
                executable_path=self.executable_path,
                accept_downloads=True,
                downloads_path=self.download_path,
            )

        else:
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.profile_path,
                headless=False,
                channel=self.browser_name,
                accept_downloads=True,
                downloads_path=self.download_path,
            )

        self.page = self.context.pages[0]

        self.home_page = HomePage(self.page)

        return self

    async def close_session(self):
        print('Đóng phiên')

        if self.context:
            await self.context.close()

        # KHÔNG context.close()
        # vì sẽ đóng luôn Chrome thật.
        # if self.browser:
        #     await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

    async def clear_cache(self):
        """Xóa browser cache."""
        print('Xóa cache')
        await self.page.goto(
            url='chrome://settings/clearBrowserData'
        )

        # LAST_15_MIN = self.page.get_by_role("button", name="Last 15 min")
        LAST_HOUR = self.page.get_by_role("button", name="Last hour")
        await LAST_HOUR.click()
        # LAST_24_HOURS = self.page.get_by_role("button", name="Last 24 hours")
        # LAST_7_DAYS = self.page.get_by_role("button", name="Last 7 days")

        DELETE_DATA = self.page.get_by_role("button", name="Delete data")
        await DELETE_DATA.click()

