import re
from src.infrastructure.auto_sent_gg_flow.base_page import BasePage
from playwright.async_api import Page


class AddReferenceComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.images = page.get_by_role("tab", name="image Images")
        self.filter_drop_down = page.get_by_role(
            "button",
            name=re.compile(
                r"^(Recent|Newest|Oldest|Most Used|Favorites)\s+arrow_drop_down$"
            )
        )
        self.newest_btn = page.get_by_role("menuitem", name="Newest")
        self.add_to_prompt = page.get_by_role("button", name="Add to Prompt")

    async def add_latest_image(self):
        '''Thêm image mới nhất được tạo vào trong prompt'''
        if self.images.get_attribute("aria-selected") != "true":
            await self.random_time_click(self.images, 'Image tab trong khu vực tham chiếu')
        await self.random_time_click(self.filter_drop_down, 'Danh sách thả xuống')
        await self.random_time_click(self.newest_btn, 'Ảnh mới nhất')
        await self.random_time_click(self.add_to_prompt, 'Thêm vào prompt')
        await self.close_component()
        return True
