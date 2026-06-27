import uuid
from datetime import datetime

from pydantic import BaseModel


class PlacementQuestionOut(BaseModel):
    question: str
    options: list[str]


class PlacementSubmitIn(BaseModel):
    answers: list[str]


class PlacementResultOut(BaseModel):
    id: uuid.UUID
    result_level: str
    score: int
    unlocked_stacks: list[str]
    completed_at: datetime

    class Config:
        from_attributes = True
