from pydantic import BaseModel


class QuizQuestionOut(BaseModel):
    question: str
    options: list[str]


class QuizSubmitIn(BaseModel):
    answers: list[int]


class QuizResultOut(BaseModel):
    direction_slug: str
    direction_title: str
    direction_icon: str
    description: str
    course_slug: str | None
    scores: dict[str, int]
    explanation: str
