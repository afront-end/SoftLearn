from uuid import UUID

from sqlalchemy.orm import Session

from models.lesson import Lesson
from models.stack import Stack


def get_by_slug(db: Session, slug: str) -> Lesson | None:
    return db.query(Lesson).filter(Lesson.slug == slug).first()


def get_for_stack(db: Session, stack_id: UUID) -> list[Lesson]:
    return db.query(Lesson).filter(Lesson.stack_id == stack_id).order_by(Lesson.order).all()


def get_stack_by_slug(db: Session, slug: str) -> Stack | None:
    return db.query(Stack).filter(Stack.slug == slug).first()
