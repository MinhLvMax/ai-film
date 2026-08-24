import random
from playwright.sync_api import Locator


def random_time_click(
        locator: Locator,
        min_delay: float = 0.2,
        max_delay: float = 0.8,
        message='Click nút gì đó...'
):
    self.page.wait_for_timeout(
        random.uniform(min_delay, max_delay) * 1000
    )

    try:
        print(f"[CLICK] {message}")
    except Exception:
        print("[CLICK] <cannot get html>")

    locator.click()
