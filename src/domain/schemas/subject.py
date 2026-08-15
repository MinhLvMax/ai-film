from pydantic import BaseModel


class Subject(BaseModel):
    name: str
    description: str


class ListSubject(BaseModel):
    '''Class này chỉ để làm cái cho llm trả về thôi'''
    characters: list[Subject]
