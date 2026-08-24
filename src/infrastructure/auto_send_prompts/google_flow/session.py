from playwright.sync_api import sync_playwright
from src.config import Config
from src.infrastructure.auto_send_prompts.google_flow.home_page.home import Home


class GoogleFlowSession:
    def __init__(self, user_profile=None, download_path=None):
        profile_path = user_profile or Config.BROWSER_PROFILES
        down_path = download_path or Config.BROWSER_DOWNLOAD_PATH
        self.context = sync_playwright().start().chromium.launch_persistent_context(
            user_data_dir=profile_path,
            headless=False,
            channel="chrome",
            accept_downloads=True,
            downloads_path=down_path
        )
        self.page = self.context.pages[0]
        self.home_page = Home(self.page)

    def close(self):
        self.context.close()


if __name__ == '__main__':
    session = GoogleFlowSession()
    session.home_page.go()
    session.page.pause()
