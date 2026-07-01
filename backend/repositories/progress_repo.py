from uuid import UUID

from sqlalchemy.orm import Session

from models.progress import ProgressStatus, UserProgress
from models.stack_progress import StackProgress


def get_stack_progress_map(db: Session, user_id: UUID, stack_ids: list[UUID]) -> dict[UUID, str]:
    rows = (
        db.query(StackProgress)
        .filter(StackProgress.user_id == user_id, StackProgress.stack_id.in_(stack_ids))
        .all()
    )
    return {row.stack_id: row.status.value for row in rows}


def unlock_stack(db: Session, user_id: UUID, stack_id: UUID) -> StackProgress:
    progress = StackProgress(user_id=user_id, stack_id=stack_id, status=ProgressStatus.in_progress)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def complete_stack(db: Session, user_id: UUID, stack_id: UUID) -> None:
    row = (
        db.query(StackProgress)
        .filter(StackProgress.user_id == user_id, StackProgress.stack_id == stack_id)
        .first()
    )
    if row:
        row.status = ProgressStatus.completed
        db.commit()


def set_stack_status(db: Session, user_id: UUID, stack_id: UUID, status: ProgressStatus) -> StackProgress:
    row = (
        db.query(StackProgress)
        .filter(StackProgress.user_id == user_id, StackProgress.stack_id == stack_id)
        .first()
    )
    if not row:
        row = StackProgress(user_id=user_id, stack_id=stack_id)
        db.add(row)
    row.status = status
    db.commit()
    db.refresh(row)
    return row


def get_lesson_progress_map(db: Session, user_id: UUID, lesson_ids: list[UUID]) -> dict[UUID, UserProgress]:
    rows = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == user_id, UserProgress.lesson_id.in_(lesson_ids))
        .all()
    )
    return {row.lesson_id: row for row in rows}


def get_lesson_progress(db: Session, user_id: UUID, lesson_id: UUID) -> UserProgress | None:
    return (
        db.query(UserProgress)
        .filter(UserProgress.user_id == user_id, UserProgress.lesson_id == lesson_id)
        .first()
    )


def unlock_lesson(db: Session, user_id: UUID, lesson_id: UUID) -> UserProgress:
    progress = UserProgress(user_id=user_id, lesson_id=lesson_id, status=ProgressStatus.in_progress)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def mark_lesson_read(db: Session, user_id: UUID, lesson_id: UUID) -> UserProgress:
    progress = get_lesson_progress(db, user_id, lesson_id)
    if not progress:
        progress = UserProgress(user_id=user_id, lesson_id=lesson_id, status=ProgressStatus.in_progress)
        db.add(progress)
    progress.lesson_read = True
    db.commit()
    db.refresh(progress)
    return progress


def complete_lesson(db: Session, user_id: UUID, lesson_id: UUID) -> UserProgress:
    progress = get_lesson_progress(db, user_id, lesson_id)
    if not progress:
        progress = UserProgress(user_id=user_id, lesson_id=lesson_id)
        db.add(progress)
    progress.practice_done = True
    progress.status = ProgressStatus.completed
    db.commit()
    db.refresh(progress)
    return progress


def count_completed_lessons(db: Session, user_id: UUID, lesson_ids: list[UUID]) -> int:
    if not lesson_ids:
        return 0
    return (
        db.query(UserProgress)
        .filter(
            UserProgress.user_id == user_id,
            UserProgress.lesson_id.in_(lesson_ids),
            UserProgress.status == ProgressStatus.completed,
        )
        .count()
    )


def get_all_stack_progress(db: Session, user_id: UUID) -> list[StackProgress]:
    return db.query(StackProgress).filter(StackProgress.user_id == user_id).all()


def get_completed_lesson_counts(db: Session, user_id: UUID, stack_ids: list[UUID]) -> dict[UUID, int]:
    from models.lesson import Lesson
    from sqlalchemy import func

    if not stack_ids:
        return {}

    rows = (
        db.query(Lesson.stack_id, func.count(UserProgress.id))
        .join(UserProgress, UserProgress.lesson_id == Lesson.id)
        .filter(
            UserProgress.user_id == user_id,
            UserProgress.status == ProgressStatus.completed,
            Lesson.stack_id.in_(stack_ids),
        )
        .group_by(Lesson.stack_id)
        .all()
    )
    return {stack_id: count for stack_id, count in rows}
