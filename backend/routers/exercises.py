from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from schemas.exercise import ExerciseCheckIn, ExerciseCheckOut, ExerciseOut
from services import auth_service, exercise_service

router = APIRouter(tags=["exercises"])


@router.get("/api/lessons/{slug}/exercises", response_model=list[ExerciseOut])
def get_exercises(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return exercise_service.get_lesson_exercises(db, slug)


@router.post("/api/exercises/{exercise_id}/check", response_model=ExerciseCheckOut)
async def check_exercise(
    exercise_id: UUID,
    payload: ExerciseCheckIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await exercise_service.check_exercise(db, exercise_id, payload.answer)
