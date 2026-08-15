from pydantic import BaseModel
from src.domain.schemas.subject import Subject
from src.domain.schemas.shot import Shot


class FilmPlan(BaseModel):
    characters: list[Subject]
    style_lock: str
    shots: list[Shot]
