import uuid
from typing import Optional

from pydantic import BaseModel

from schemas.stack import StackWithProgress


class CourseOut(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None
    order: int

    class Config:
        from_attributes = True


class CourseWithStacks(CourseOut):
    stacks: list[StackWithProgress] = []
