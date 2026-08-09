from src.application.dto.gen_content_dto import (
    GenContentInput,
    GenContentOutput,
)
from src.application.gen_content import GenContent


class GenContentController:
    def __init__(self, use_case: GenContent):
        self.use_case = use_case

    def generate(
            self,
            keyword: str,
            description: str,
            system_prompt: str,
            gen_toc_prompt: str,
            gen_chapter_prompt: str,
            sources: list[str],
    ) -> GenContentOutput:
        input_data = GenContentInput(
            title=keyword,
            description=description,
            system_prompt=system_prompt,
            gen_toc_prompt=gen_toc_prompt,
            gen_chapter_prompt=gen_chapter_prompt,
            sources=sources,
        )
        return self.use_case.gen(input_data)
