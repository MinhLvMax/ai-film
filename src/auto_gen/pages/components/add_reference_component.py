import re
from src.auto_gen.pages.components.base_component import BaseComponent


class AddReferenceComponent(BaseComponent):
    def __init__(self, page):
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

    def add_latest_image(self):
        if self.images.get_attribute("aria-selected") != "true":
            self.random_time_click(self.images)
        self.random_time_click(self.filter_drop_down)
        self.random_time_click(self.newest_btn)
        self.random_time_click(self.add_to_prompt)
        self.close_component()
        return True
