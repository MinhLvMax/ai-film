from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from src.infrastructure.auto_sent_gg_flow.base_page import BasePage
from src.infrastructure.auto_sent_gg_flow.home_page.project_page import ProjectPage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.URL = 'https://labs.google/fx/tools/flow'
        self.CREATE_WITH_GG_FLOW = page.get_by_role("button", name="Create with Google Flow")
        self.NEW_PROJECT = page.get_by_role("button", name="add_2 New project")

    async def create_with_google_flow(self):
        '''Nếu có thì ấn nút trắng create with google flow, không có thì thôi'''
        if await self.CREATE_WITH_GG_FLOW.is_visible():
            await self.random_time_click(self.CREATE_WITH_GG_FLOW, msg='Create with Google Flow')

            await self.CREATE_WITH_GG_FLOW.click(
                no_wait_after=True
            )

            await self.page.wait_for_url(
                "**/fx/tools/flow**",
                wait_until="commit",
                timeout=30_000,
            )

    async def open_or_create_new_project(self, project_name):
        '''Mở hoặc tạo mới 1 project theo tên'''
        await self.create_with_google_flow()
        # self.page.pause()
        if await self._is_exist_project(project_name):
            return await self._open_exist_project_page(project_name)
        else:
            return await self._create_new_project(project_name)

    async def _open_exist_project_page(self, project_name):
        '''Mở 1 project đã có sẵn'''
        span = self.page.get_by_text(f"{project_name}editEdit project")
        a = span.locator("xpath=ancestor::div[2]/a")
        await self.random_time_click(a, msg='Đi vào project')
        await self.wait_util_loaded()
        return ProjectPage(self.page)

    async def _create_new_project(self, project_name):
        await self.random_time_click(self.NEW_PROJECT, msg='Tạo mới project')
        await self.wait_util_loaded()
        new_project_page = ProjectPage(self.page)
        await new_project_page.set_project_name(project_name)
        # Chuyển sang page mới thì mới return page mới
        return new_project_page

    async def _is_exist_project(self, project_name):
        '''Tìm và trả về locator của project đã tồn tại trước đó với project_name, thêm độ trễ nghỉ để locator kịp load ra'''
        locator = self.page.get_by_text(
            f"{project_name}editEdit project"
        )
        try:
            await locator.wait_for(
                state="visible",
                timeout=5000
            )
            return True

        except PlaywrightTimeoutError:
            return False
