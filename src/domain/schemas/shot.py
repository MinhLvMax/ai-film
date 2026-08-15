from pydantic import BaseModel
from src.domain.schemas.camera import Camera
from src.domain.schemas.subject import Subject


class ShotLLMResult(BaseModel):
    '''Class này là để model trả về những key cần thiết'''
    shot_id: str
    subject_ids: list[str]
    action: str
    environment: str


class Shot(BaseModel):
    '''Class này là để khi lưu json'''
    shot_id: str
    subject: list[Subject]
    action: str
    environment: str
    camera: Camera
