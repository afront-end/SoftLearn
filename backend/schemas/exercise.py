import uuid
from typing import Optional

from pydantic import BaseModel


class ExerciseOut(BaseModel):
    id: uuid.UUID
    type: str
    question: str
    options: Optional[list[str]] = None
    order: int

    class Config:
        from_attributes = True


class ExerciseCheckIn(BaseModel):
    answer: str


class ExerciseCheckOut(BaseModel):
    correct: bool
    explanation: Optional[str] = None
    correct_answer: Optional[str] = None
