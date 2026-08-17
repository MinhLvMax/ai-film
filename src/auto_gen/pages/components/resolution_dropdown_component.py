from src.auto_gen.pages.components.base_component import BaseComponent
from src.auto_gen.constant.resoluion import Resolution

class ResolutionDropdownComponent(BaseComponent):
    def __init__(self, page):
        super().__init__(page)
        self.r_720p = page.get_by_role("menuitem", name="720p Original Size")
        self.r_1080p = page.get_by_role("menuitem", name="1080p Upscaled")
        self.r_4k = page.get_by_role("menuitem", name="4K Upscaled · 50 credits")

    def click_resolution(self, resolution: Resolution):
        if resolution.R_720P:
            self.random_time_click(self.r_720p)
        elif resolution.R_1080P:
            self.random_time_click(self.r_1080p)
        elif resolution.R_4K:
            self.random_time_click(self.r_4k)