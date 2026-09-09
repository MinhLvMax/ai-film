from src.application.use_case.analysis_script import AnalysisScript
from src.application.use_case.login_profile import login_profile


class UICapabilities:
    def __init__(self, analysis_script: AnalysisScript, build_prompt_method, send_prompt_method):
        self.analysis_script = analysis_script
        self.build_prompt_method = build_prompt_method
        self.send_prompt_method = send_prompt_method
        # self.login_profile = login_profile

    def analyze_script(self, content, extract_char_prompt, extract_shot_prompt):
        # chars = self.analysis_script.extract_chars(extract_char_prompt, content)
        # shots = self.analysis_script.extract_shots_for_section(extract_shot_prompt, content)
        # return chars, shots
        pass

    async def send_prompts(self,
                           prompts,
                           generation_mode,
                           ratio,
                           quantity,
                           duration,
                           model,
                           max_creating_video,
                           project_name,
                           ):
        '''Gửi prompt để tạo các video'''
        async for update_prompts in self.send_prompt_method(
                prompts,
                generation_mode,
                ratio,
                quantity,
                duration,
                model,
                max_creating_video,
                project_name,
        ):
            yield update_prompts

    async def send_prompt_sequentiallys(self,
                                        prompts: list[dict],
                                        project_url: str,
                                        sleep_time: int,
                                        ):
        async for update_prompts in self.send_prompt_method(
                prompts,
                project_url,
                sleep_time,
        ):
            yield update_prompts

    async def extract_chars(self, prompt, model, content):
        '''Trích xuất nhân vật'''
        return await self.analysis_script.extract_chars(
            prompt=prompt,
            model=model,
            content=content
        )

    def extract_shots(self, prompt, model, content, chars):
        '''Trích xuất cảnh từ 1 đoạn của content, nên phân đoạn content ở giao diện trước để làm xong đến đâu view đến đấy'''
        return self.analysis_script.extract_shots(
            prompt=prompt,
            model=model,
            content=content,
            chars=chars,
        )

    def build_prompt(self, style_lock, chars, shots):
        '''Xây dựng prompt từ cảnh'''
        return self.build_prompt_method(style_lock, chars, shots)

    async def sign_in_google(self, browser_name=None):
        '''Đăng nhập nick mà đăng kí tài khoản google flow'''
        await login_profile(browser_name)

    async def download_last_element(self):
        '''Tải xuống 1 phần tử gần nhất, hiện tại làm là 720mb cho nhanh vì 1k 4k rất lâu'''
