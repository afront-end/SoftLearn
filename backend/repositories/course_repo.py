from sqlalchemy.orm import Session

from models.course import Course
from models.stack import Stack


def get_all(db: Session) -> list[Course]:
    return db.query(Course).order_by(Course.order).all()


def get_by_slug(db: Session, slug: str) -> Course | None:
    return db.query(Course).filter(Course.slug == slug).first()


def get_stacks_for_course(db: Session, course_id) -> list[Stack]:
    return db.query(Stack).filter(Stack.course_id == course_id).order_by(Stack.order).all()
