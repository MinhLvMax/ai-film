from pydantic import BaseModel, Field
from src.domain.schemas.table_of_contents import TableOfContents


class GenContentDTO(BaseModel):
    title: str = Field(min_length=1)
    system_prompt: str = Field(default='')
    gen_toc_prompt: str = Field(default='')
    toc: TableOfContents = Field(default=None)
    chaps: list[str] = Field(default_factory=list)
    chapter_count: int | str
    gen_chapter_prompt: str = Field(default='')
    chapter_length: int | str
    sleep_time: int = Field(ge=0)
    sources: list[str] = Field(default_factory=list)
