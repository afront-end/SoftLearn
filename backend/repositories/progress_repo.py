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
