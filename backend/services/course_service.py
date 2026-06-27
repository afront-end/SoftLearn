import json
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.redis_client import redis_client
from models.course import Course
from repositories import course_repo, progress_repo
from schemas.course import CourseOut, CourseWithStacks
from schemas.stack import StackOut, StackWithProgress

COURSES_CACHE_KEY = "courses:list"
COURSES_CACHE_TTL = 300


def list_courses(db: Session) -> list[CourseOut]:
    cached = redis_client.get(COURSES_CACHE_KEY)
    if cached:
        return [CourseOut.model_validate(c) for c in json.loads(cached)]

    courses = course_repo.get_all(db)
    courses_out = [CourseOut.model_validate(c) for c in courses]
    redis_client.set(
        COURSES_CACHE_KEY,
        json.dumps([c.model_dump(mode="json") for c in courses_out]),
        ex=COURSES_CACHE_TTL,
    )
    return courses_out


def get_course_with_stacks(db: Session, slug: str, user_id: UUID) -> CourseWithStacks:
    course = course_repo.get_by_slug(db, slug)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Курс не найден")

    stacks = course_repo.get_stacks_for_course(db, course.id)
    progress_map = progress_repo.get_stack_progress_map(db, user_id, [s.id for s in stacks])

    if stacks and not progress_map:
        progress_repo.unlock_stack(db, user_id, stacks[0].id)
        progress_map[stacks[0].id] = "in_progress"

    stacks_out = [
        StackWithProgress(**StackOut.model_validate(s).model_dump(), status=progress_map.get(s.id, "locked"))
        for s in stacks
    ]
    return CourseWithStacks(**CourseOut.model_validate(course).model_dump(), stacks=stacks_out)
