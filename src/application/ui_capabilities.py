from src.application.use_case.analysis_script import AnalysisScript


class UICapabilities:
    def __init__(self, analysis_script: AnalysisScript, send_prompts):
        self.analysis_script = analysis_script
        self.send_prompts = send_prompts

    def analyze_script(self, content, extract_char_prompt, extract_shot_prompt):
        # chars = self.analysis_script.extract_chars(extract_char_prompt, content)
        # shots = self.analysis_script.extract_shots_for_section(extract_shot_prompt, content)
        # return chars, shots
        pass

    def send_prompts(self, prompts):
        self.send_prompts(prompts)

    def extract_chars(self, prompt, model, content):
        '''Trích xuất nhân vật'''
        return self.analysis_script.extract_chars(
            prompt=prompt,
            model=model,
            content=content
        )

    def extract_shots(self, prompt, model, section, title, chars):
        '''Trích xuất cảnh'''
        self.analysis_script.extract_shots_for_section(
            prompt=prompt,
            section=section,
            title=title,
            model=model,
            chars=chars
        )

    def build_prompt(self, shots):
        '''Xây dựng prompt từ cảnh'''

    def sign_in_google(self):
        '''Đăng nhập nick mà đăng kí tài khoản google flow'''
