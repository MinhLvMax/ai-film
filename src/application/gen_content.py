from src.application.ports.llm_port import LLMService
from src.application.ports.logger_port import LoggerService
from src.domain.prompt_factory.prompt_factory import FormatStringFactory


class GenContent:
    def __init__(self, llm: LLMService, logger: LoggerService, format_string: FormatStringFactory):
        self.llm = llm
        self.logger = logger
        self.format_string = format_string

    def gen(self, keyword, description) -> str:
        '''
        Sinh nội dung dựa trên chủ đề và mô tả đầu vào.
        :param keyword: Chủ đề chính cần sinh nội dung.
        :param description: Thông tin mô tả bổ sung giúp định hướng nội dung.
        :return:  Nội dung được sinh từ mô hình ngôn ngữ.
        '''
        prompt = self.format_string.gen_content_prompt(keyword, description)
        content = self.llm.complete(prompt)
        return content
