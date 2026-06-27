from uuid import UUID

from sqlalchemy.orm import Session

from models.placement_test import PlacementLevel, PlacementTest


def add_result(
    db: Session, user_id: UUID, course_id: UUID, result_level: PlacementLevel, score: int, answers: list[str]
) -> PlacementTest:
    result = PlacementTest(
        user_id=user_id, course_id=course_id, result_level=result_level, score=score, answers=answers
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
