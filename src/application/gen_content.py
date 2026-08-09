import time
from src.application.llm_service import LLM
from src.application.ports.file_reader_port import FileReaderPort
from src.application.logger_service import LoggerService
from src.application.context_manager import ContextManager
from src.application.dto.gen_content_dto import GenContentInput, GenContentOutput
from src.application.prompt_builder import PromptBuilder
from src.domain.schemas.table_of_contents import TableOfContents


class GenContent:
    def __init__(
            self,
            gen_toc_llm: LLM | None = None,
            gen_chap_llm: LLM | None = None,
            logger: LoggerService | None = None,
            sleep_time: int = 0,
            context_manager: ContextManager | None = None,
            prompt_builder: PromptBuilder | None = None,
            file_reader: FileReaderPort | None = None,
    ):
        self.gen_toc_llm = gen_toc_llm
        self.gen_chap_llm = gen_chap_llm
        self.logger = logger
        self.sleep_time = sleep_time
        self.context_manager = context_manager or ContextManager()
        self.prompt_builder = prompt_builder or PromptBuilder(file_reader)
        pass

    def gen(self, input: GenContentInput):
        self.logger.info(self.gen.__name__)
        gen_toc_prompt = self.prompt_builder.get_prompt('toc', )
        toc_json = self.gen_toc_llm.complete(
            messages=gen_toc_prompt, response_model=TableOfContents
        )
        toc = TableOfContents.model_validate(toc_json)

        chapter_contents = []
        for chap in toc.chapters:
            gen_chap_prompt = self.format_string_factory.gen_chap_prompt(
                toc=toc_json, chapter=str(chap.model_dump())
            )
            chapter_contents.append(self.gen_chap_llm.complete(gen_chap_prompt))
            time.sleep(self.sleep_time)

        # Ghép nội dung
        full_content = self.format_string_factory.full_content(
            gen_toc_model=self.gen_toc_llm.default_model,
            gen_chap_model=self.gen_chap_llm.default_model,
            title=toc.title,
            description=toc.description,
            content=chapter_contents,
        )
        return GenContentOutput(
            full_content=full_content
        )
