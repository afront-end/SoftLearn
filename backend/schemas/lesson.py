import uuid
from typing import Optional

from pydantic import BaseModel


class LessonOut(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    order: int

    class Config:
        from_attributes = True


class LessonWithProgress(LessonOut):
    status: str = "locked"
    lesson_read: bool = False
    practice_done: bool = False


class LessonDetail(LessonOut):
    content: Optional[str] = None
    stack_slug: str
    stack_title: str
    lesson_read: bool = False
    practice_done: bool = False


class StackLessonsOut(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: Optional[str] = None
    lessons: list[LessonWithProgress] = []
