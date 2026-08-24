import json
from src.application.ports.file_reader_port import FileReaderPort
from src.application.ports.llm_port import LLM


class GenPrompt:
    def __init__(self, file_reader: FileReaderPort, llm: LLM, gen_prompt_from_segment_path: str):
        self.llm = llm
        self.file_reader = file_reader
        self.gen_prompt_from_segment_path = gen_prompt_from_segment_path

    async def gen_prompt_from_a_segment(self, segment_content: str):
        '''
        Nhận đoạn từ phía UI để gen ra bộ prompt cho đoạn đó
        :param segment_content:
        :return:
        '''
        gen_prompt_from_segment = self.file_reader.read(self.gen_prompt_from_segment_path).format(
            screenplay_segment=segment_content)
        complete_result = await self.llm.complete(gen_prompt_from_segment)
        return json.loads(complete_result.content)

