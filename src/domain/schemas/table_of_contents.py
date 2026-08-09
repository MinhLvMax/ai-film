from pydantic import BaseModel, Field


class Chapter(BaseModel):
    name: str = Field(min_length=1, description="Tên của chương.")
    summary: str = Field(..., description="Nội dung tóm tắt của chương.")


class TableOfContents(BaseModel):
    title: str = Field(..., description="Tiêu đề của tài liệu.")

    description: str = Field(
        ..., description="Mô tả ngắn gọn về nội dung và phạm vi của tài liệu."
    )

    chapters: list[Chapter] = Field(
        ..., description="Danh sách các chương của tài liệu theo đúng thứ tự."
    )

    def get_outline(self) -> str:
        outline = ""

        for chapter in self.chapters:
            outline += f"- {chapter.title}: {chapter.summary}\n"

        return outline
