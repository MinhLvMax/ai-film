import time
from src.application.ports.llm_port import LLM
from src.application.logger_service import LoggerService
from src.application.context_manager import ContextManager, Message
from src.application.dto.gen_content_dto import GenContentDTO
from src.application.llm_complete_results import CompleteResult
from src.domain.schemas.table_of_contents import TableOfContents
from src.domain.format_string.prompt_factory import GenTOCPrompt, GenChapPrompt


class GenContent:
    def __init__(
            self,
            gen_toc_llm: LLM | None = None,  # 2 model này về sau phải nhận từ UI
            gen_chap_llm: LLM | None = None,
            logger: LoggerService | None = None,
            context_manager: ContextManager | None = None,
    ):
        self.gen_toc_llm = gen_toc_llm
        self.gen_chap_llm = gen_chap_llm
        self.logger = logger
        self.context_manager = context_manager
        pass

    def gen_toc(self, input: GenContentDTO):
        gen_toc_prompt_msg = Message(  # Gán ra ngoài đối tượng để chút nữa xóa đối tượng khỏi lịch sử
            role='user',
            content=input.gen_toc_prompt + GenTOCPrompt(
                keyword=input.title,
                chapter_count=input.chapter_count,
            )
        )
        self.context_manager.add_message(gen_toc_prompt_msg)
        complete_result = self.gen_toc_llm.complete(
            messages=self.context_manager.get_dict_history(), response_model=TableOfContents
        )
        # Xóa prompt toc user đi để tiết kiệm token và chú tâm vào nội dung gen
        self.context_manager.remove_message(gen_toc_prompt_msg)
        toc: TableOfContents = complete_result.response_model
        self.logger.debug(str(toc))
        return toc

    def gen_chap(self, input: GenContentDTO):
        chapter_contents = []
        for chap in input.toc.chapters:
            gen_chap_prompt_msg = Message(
                role='user',
                content=input.gen_chapter_prompt + GenChapPrompt(
                    chapter_name=chap.name,
                    chapter_summary=chap.summary,
                    target_length=input.chapter_length,
                )
            )
            self.context_manager.add_message(gen_chap_prompt_msg)  # Thêm vào lịch sử dùng xong thì xóa
            complete_result: CompleteResult = self.gen_chap_llm.complete(self.context_manager.get_dict_history())
            chapter_content = complete_result.content
            self.logger.debug(f'{chapter_content=}')
            self.context_manager.remove_message(gen_chap_prompt_msg)

            chapter_contents.append(chapter_content)
            time.sleep(input.sleep_time)

        return chapter_contents

    def gen(self, input: GenContentDTO):
        # Gán system prompt
        system_prompt = input.system_prompt
        self.context_manager.add_message(Message(
            role='system',
            content=system_prompt,
        ))

        toc = self.gen_toc(input)

        self.context_manager.add_message(Message(  # Thêm nội dung toc vào lịch sử chat
            role='assistant',
            content=str(toc.model_dump()),
        ))
        input.toc = toc
        chaps = self.gen_chap(input)

        input.toc = toc
        input.chaps = chaps

        return input
