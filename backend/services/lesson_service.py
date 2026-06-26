from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories import lesson_repo, progress_repo
from schemas.lesson import LessonDetail, LessonOut, LessonWithProgress, StackLessonsOut


def get_stack_lessons(db: Session, stack_slug: str, user_id: UUID) -> StackLessonsOut:
    stack = lesson_repo.get_stack_by_slug(db, stack_slug)
    if not stack:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Стек не найден")

    lessons = lesson_repo.get_for_stack(db, stack.id)
    progress_map = progress_repo.get_lesson_progress_map(db, user_id, [l.id for l in lessons])

    if lessons and lessons[0].id not in progress_map:
        progress_map[lessons[0].id] = progress_repo.unlock_lesson(db, user_id, lessons[0].id)

    lessons_out = []
    for lesson in lessons:
        progress = progress_map.get(lesson.id)
        lessons_out.append(
            LessonWithProgress(
                **LessonOut.model_validate(lesson).model_dump(),
                status=progress.status.value if progress else "locked",
                lesson_read=progress.lesson_read if progress else False,
                practice_done=progress.practice_done if progress else False,
            )
        )

    return StackLessonsOut(
        id=stack.id, title=stack.title, slug=stack.slug, description=stack.description, lessons=lessons_out
    )


def get_lesson_detail(db: Session, slug: str, user_id: UUID) -> LessonDetail:
    lesson = lesson_repo.get_by_slug(db, slug)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")

    progress = progress_repo.get_lesson_progress(db, user_id, lesson.id)
    if not progress:
        siblings = lesson_repo.get_for_stack(db, lesson.stack_id)
        if siblings and siblings[0].id == lesson.id:
            progress = progress_repo.unlock_lesson(db, user_id, lesson.id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Урок заблокирован")

    return LessonDetail(
        id=lesson.id,
        title=lesson.title,
        slug=lesson.slug,
        order=lesson.order,
        content=lesson.content,
        stack_slug=lesson.stack.slug,
        stack_title=lesson.stack.title,
        lesson_read=progress.lesson_read,
        practice_done=progress.practice_done,
    )


def mark_lesson_read(db: Session, slug: str, user_id: UUID) -> LessonDetail:
    lesson = lesson_repo.get_by_slug(db, slug)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")

    progress = progress_repo.mark_lesson_read(db, user_id, lesson.id)

    siblings = lesson_repo.get_for_stack(db, lesson.stack_id)
    idx = next((i for i, l in enumerate(siblings) if l.id == lesson.id), None)
    if idx is not None and idx + 1 < len(siblings):
        next_lesson = siblings[idx + 1]
        if not progress_repo.get_lesson_progress(db, user_id, next_lesson.id):
            progress_repo.unlock_lesson(db, user_id, next_lesson.id)

    return LessonDetail(
        id=lesson.id,
        title=lesson.title,
        slug=lesson.slug,
        order=lesson.order,
        content=lesson.content,
        stack_slug=lesson.stack.slug,
        stack_title=lesson.stack.title,
        lesson_read=progress.lesson_read,
        practice_done=progress.practice_done,
    )
