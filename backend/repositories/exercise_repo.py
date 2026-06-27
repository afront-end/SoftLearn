from uuid import UUID

from sqlalchemy.orm import Session

from models.exercise import Exercise


def get_for_lesson(db: Session, lesson_id: UUID) -> list[Exercise]:
    return db.query(Exercise).filter(Exercise.lesson_id == lesson_id).order_by(Exercise.order).all()


def get_by_id(db: Session, exercise_id: UUID) -> Exercise | None:
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()
