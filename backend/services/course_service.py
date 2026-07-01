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

# "Fullstack" — витрина без собственных стеков: объединяет стеки Frontend и Backend,
# прогресс при этом всё равно общий (StackProgress хранится по stack_id, а не по курсу).
COMBINED_COURSE_SLUGS: dict[str, list[str]] = {
    "fullstack": ["frontend", "backend"],
}


def get_stacks_for_course(db: Session, course: Course) -> list:
    source_slugs = COMBINED_COURSE_SLUGS.get(course.slug)
    if not source_slugs:
        return course_repo.get_stacks_for_course(db, course.id)

    stacks = []
    for slug in source_slugs:
        source_course = course_repo.get_by_slug(db, slug)
        if source_course:
            stacks.extend(course_repo.get_stacks_for_course(db, source_course.id))
    return stacks


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

    stacks = get_stacks_for_course(db, course)
    progress_map = progress_repo.get_stack_progress_map(db, user_id, [s.id for s in stacks])

    if stacks and not progress_map:
        progress_repo.unlock_stack(db, user_id, stacks[0].id)
        progress_map[stacks[0].id] = "in_progress"

    lesson_counts = {s.id: len(s.lessons) for s in stacks}
    completed_counts = progress_repo.get_completed_lesson_counts(db, user_id, [s.id for s in stacks])

    stacks_out = [
        StackWithProgress(
            **StackOut.model_validate(s).model_dump(),
            status=progress_map.get(s.id, "locked"),
            lesson_count=lesson_counts.get(s.id, 0),
            completed_count=completed_counts.get(s.id, 0),
        )
        for s in stacks
    ]
    return CourseWithStacks(**CourseOut.model_validate(course).model_dump(), stacks=stacks_out)
