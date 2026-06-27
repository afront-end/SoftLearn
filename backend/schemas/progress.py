import uuid

from pydantic import BaseModel


class CourseProgressOut(BaseModel):
    course_id: uuid.UUID
    course_title: str
    course_slug: str
    course_icon: str | None = None
    stacks_completed: int
    stacks_total: int
    lessons_completed: int
    lessons_total: int


class ProgressOverviewOut(BaseModel):
    courses: list[CourseProgressOut]
    stacks_completed_total: int
    lessons_completed_total: int


class StackProgressEntryOut(BaseModel):
    course_title: str
    course_slug: str
    stack_title: str
    stack_slug: str
    status: str
