import re
from src.application.ports.llm_port import LLM
from src.application.ports.file_reader_port import FileReaderPort
from src.application.ports.file_writer_port import FileWriterPort
from src.domain.schemas.screen_play_section import ScreenplaySection
from src.domain.schemas.subject import ListSubject
from src.config import Config


class CreateFilmPlan:
    def __init__(self, llm: LLM, file_reader: FileReaderPort, file_writer: FileWriterPort, screen_play_path):
        self.llm = llm
        self.file_reader = file_reader
        self.file_writer = file_writer
        self.screenplay = file_reader.read(screen_play_path)
        self.sections: list[ScreenplaySection] = []

    def _sreenplay_chunking(self):
        pattern = re.compile(
            r'(?m)^[A-ZÁÉÍÓÚÜÑ0-9][A-ZÁÉÍÓÚÜÑ0-9\s:,\-–—\'".!?()&]+$'
        )

        matches = list(pattern.finditer(self.screenplay))

        chunks = []

        # Content trước section đầu tiên
        if matches and self.screenplay[:matches[0].start()].strip():
            chunks.append({
                "title": None,
                "content": self.screenplay[:matches[0].start()].strip(),
            })

        for i, match in enumerate(matches):
            title = match.group().strip()

            start = match.end()
            end = (
                matches[i + 1].start()
                if i + 1 < len(matches)
                else len(self.screenplay)
            )

            chunks.append({
                "title": title,
                "content": self.screenplay[start:end].strip(),
            })

        return chunks

    def _extract_character(self, extract_char_prompt_path):
        extract_char_prompt = self.file_reader.read(extract_char_prompt_path)
        complete_result = self.llm.complete(extract_char_prompt.format(screenplay=self.screenplay), ListSubject)
        print(complete_result.response_model.model_dump())
        pass


if __name__ == '__main__':
    pass
