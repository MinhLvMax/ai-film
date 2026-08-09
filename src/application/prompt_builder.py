from typing import Literal
from src.application.ports.file_reader_port import FileReaderPort
from src.config import Config


class PromptBuilder:
    def __init__(self, file_reader: FileReaderPort):
        self.file_reader = file_reader
        self.map = {
            'system': Config.PROMPTS / 'system_prompt.txt',
            'toc': Config.PROMPTS / 'gentoc_prompt.txt',
            'chap': Config.PROMPTS / 'genchap_prompt.txt',
        }


    def get_prompt(self, name: Literal['system', 'toc', 'chap'], additional_info: str | None = None):
        prompt_path = self.map.get(name)
        return self.file_reader.read(prompt_path) + additional_info if additional_info else ''

if __name__ == '__main__':
    from src.domain import prompt_factory
    from src.infrastructure.text_reader import TextReader
    file_reader = TextReader()
    prompt_builder = PromptBuilder(file_reader)

    # additional_info = prompt_factory.GenTOCPrompt(
    #     keyword='Du lịch Việt Nam',
    #     chapter_count=5
    # )

    additional_info = prompt_factory.GenChapPrompt(
        chapter_name='Chương 1',
        target_length=500,
        chapter_summary='Ngày xửa ngày xưa ... ...'
    )

    print(prompt_builder.get_prompt('chap', additional_info))


