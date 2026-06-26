from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.course import Course
from repositories import course_repo, progress_repo
from schemas.course import CourseOut, CourseWithStacks
from schemas.stack import StackOut, StackWithProgress


def list_courses(db: Session) -> list[Course]:
    return course_repo.get_all(db)


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
