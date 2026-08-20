from pydantic import BaseModel, Field


class SubjectLLMResult(BaseModel):
    name: str = Field(
        description="Tên của nhân vật hoặc đối tượng xuất hiện trong nội dung."
    )
    description: str = Field(
        description="Mô tả chi tiết về ngoại hình, đặc điểm nhận dạng và các thuộc tính quan trọng của nhân vật hoặc đối tượng."
    )


class ListSubjectLLMResult(BaseModel):
    '''Class này chỉ để làm cái cho llm trả về thôi'''
    list_subjects: list[SubjectLLMResult] = Field(
        description="Danh sách tất cả nhân vật hoặc đối tượng quan trọng xuất hiện trong nội dung."
    )


class Subject(SubjectLLMResult):
    id: str
