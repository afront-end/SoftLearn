from uuid import UUID

from sqlalchemy.orm import Session

from models.test import Test
from models.test_result import TestResult


def get_for_lesson(db: Session, lesson_id: UUID) -> Test | None:
    return db.query(Test).filter(Test.lesson_id == lesson_id).first()


def get_attempt_count(db: Session, user_id: UUID, test_id: UUID) -> int:
    return db.query(TestResult).filter(TestResult.user_id == user_id, TestResult.test_id == test_id).count()


def add_result(
    db: Session, user_id: UUID, test_id: UUID, score: int, passed: bool, mistakes: list[dict], attempt: int
) -> TestResult:
    result = TestResult(
        user_id=user_id, test_id=test_id, score=score, passed=passed, mistakes=mistakes, attempt=attempt
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_results(db: Session, user_id: UUID, test_id: UUID) -> list[TestResult]:
    return (
        db.query(TestResult)
        .filter(TestResult.user_id == user_id, TestResult.test_id == test_id)
        .order_by(TestResult.created_at)
        .all()
    )
