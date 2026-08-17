from src.auto_gen.pages.components.base_component import BaseComponent
from src.auto_gen.pages.components.resolution_dropdown_component import ResolutionDropdownComponent
from src.auto_gen.constant.resoluion import Resolution

class RightClickMenuComponent(BaseComponent):
    def __init__(self, page):
        super().__init__(page)
        self.down_load_btn = page.get_by_text("downloadDownload")

    def download_this_video(self, resolution: Resolution):
        self.random_time_click(self.down_load_btn)
        resolution_dropdown = ResolutionDropdownComponent(self.page)
        resolution_dropdown.click_resolution(resolution)
        return True

