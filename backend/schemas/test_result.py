import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TestQuestionOut(BaseModel):
    question: str
    options: list[str]


class TestOut(BaseModel):
    id: uuid.UUID
    pass_threshold: int
    time_limit: Optional[int] = None
    questions: list[TestQuestionOut]


class TestSubmitIn(BaseModel):
    answers: list[str]


class MistakeOut(BaseModel):
    question: str
    user_answer: str
    correct_answer: str


class TestResultOut(BaseModel):
    id: uuid.UUID
    score: int
    passed: bool
    mistakes: list[MistakeOut]
    attempt: int
    created_at: datetime

    class Config:
        from_attributes = True
