from pydantic import BaseModel


class ScreenplaySection(BaseModel):
    '''Class để cắt phân đoạn kịch bản ra để giảm context'''
    title: str
    content: str
