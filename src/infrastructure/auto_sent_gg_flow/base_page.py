from playwright.async_api import Page, Locator
import random


class BasePage:
    def __init__(self, page: Page):
        self.page: Page = page

    async def wait_util_loaded(self):
        '''Sau mỗi lần goto sang url nào đó thì nên dùng hàm này để đợi chờ load'''
        print("Loading page...")
        await self.page.wait_for_load_state("networkidle")

    async def random_time_click(
            self,
            locator: Locator,
            msg='Click nút gì đó...',
            min_delay: float = 0.2,
            max_delay: float = 0.8,
    ):
        await locator.wait_for(state='visible')
        await self.page.wait_for_timeout(
            random.uniform(min_delay, max_delay) * 1000
        )

        print(f'[CLICK] {msg}')

        await locator.click()

    async def click_random_order(self, *locators: Locator):
        locators = list(locators)
        random.shuffle(locators)
        for locator in locators:
            if locator != None:
                await self.random_time_click(locator, msg='Thực hiện loạt thao tác')

    async def wait_for_seconds(self, seconds: float = 2):
        """
        Hard wait for fixed seconds.
        """
        await self.page.wait_for_timeout(seconds * 1000)

    async def debug_locator(self, locator: Locator):
        count = await locator.count()

        print("=" * 80)
        print(f"Count: {count}")

        for i in range(count):
            item = locator.nth(i)
            print(f"\n[{i}]")
            print("tag:", await item.evaluate("e => e.tagName"))
            print("text:", repr(item.text_content()))
            print("html:", await item.evaluate("e => e.outerHTML"))

    async def close_component(self):
        await self.page.keyboard.press('Escape')
