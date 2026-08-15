from pydantic import BaseModel


class Camera(BaseModel):
    shot_type: str
    movement: str
