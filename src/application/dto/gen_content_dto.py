from pydantic import BaseModel, Field


class GenContentInput(BaseModel):
    title: str = Field(min_length=1)
    system_prompt: str = Field(default='')
    gen_toc_prompt: str = Field(default='')
    gen_chapter_prompt: str = Field(default='')
    sources: list[str] = Field(default_factory=list)


class GenContentOutput(BaseModel):
    full_content: str = Field(default='')
