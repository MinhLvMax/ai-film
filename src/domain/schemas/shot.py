from pydantic import BaseModel
from src.domain.schemas.camera import Camera
from src.domain.schemas.subject import SubjectLLMResult


class ShotLLMResult(BaseModel):
    '''Class này là để model trả về những key cần thiết'''
    subject_ids: list[str]
    action: str
    environment: str
    camera: str


class ListShotLLMResult(BaseModel):
    '''Class này chỉ để làm cái cho llm trả về thôi'''
    shots: list[ShotLLMResult]


class Shot(ShotLLMResult):
    '''Class này là để khi lưu json'''
    shot_id: str
    # subjects: list[SubjectLLMResult]
    section: str
