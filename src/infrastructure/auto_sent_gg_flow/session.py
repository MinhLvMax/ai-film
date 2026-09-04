from playwright.async_api import async_playwright, Page

from src.config import Config
from src.infrastructure.auto_sent_gg_flow.home_page import HomePage


class GoogleFlowSession:
    CDP_HOST = "127.0.0.1"
    CDP_PORT = 9222

    def __init__(self, user_profile=None, download_path=None):
        self.profile_path = user_profile or Config.BROWSER_PROFILES
        self.download_path = download_path or Config.BROWSER_DOWNLOAD_PATH

        self.playwright = None
        self.browser = None
        self.context = None
        self.page: Page | None = None
        self.home_page = None

        self.chrome_process = None



    async def start(self):
        self.playwright = await async_playwright().start()

        # Kết nối vào Chrome đang chạy
        # self.browser = await self.playwright.chromium.connect_over_cdp(
        #     "http://127.0.0.1:9222"
        # )
        #
        # # Lấy context của Chrome thật
        # self.context = self.browser.contexts[0]
        #
        # # Lấy tab hiện tại
        # if self.context.pages:
        #     self.page = self.context.pages[0]
        # else:
        #     self.page = await self.context.new_page()

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
