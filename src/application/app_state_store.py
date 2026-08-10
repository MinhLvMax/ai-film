from typing import Protocol
from src.application.ports.file_reader_port import FileReaderPort
from src.application.ports.file_writer_port import FileWriterPort
from src.application.dto.gen_content_dto import GenContentDTO
from src.config import Config


class AppStateStore(Protocol):
    def __init__(self, file_reader: FileReaderPort, file_writer: FileWriterPort):
        self.file_reader = file_reader
        self.file_writer = file_writer
        self.prompt_paths_map = {
            'system': Config.PROMPTS / 'system_prompt.txt',
            'toc': Config.PROMPTS / 'gentoc_prompt.txt',
            'chap': Config.PROMPTS / 'genchap_prompt.txt',
        }

    def load(self, input_path) -> GenContentDTO:
        data = self.file_reader.read(input_path)
        return GenContentDTO.model_validate(data)

    def save(self, genDTO: GenContentDTO):
        self.file_writer.write(genDTO.system_prompt, self.prompt_paths_map.get('system'))
        self.file_writer.write(genDTO.gen_toc_prompt, self.prompt_paths_map.get('toc'))
        self.file_writer.write(genDTO.gen_chapter_prompt, self.prompt_paths_map.get('chap'))
        pass
