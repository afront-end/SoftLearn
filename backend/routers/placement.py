from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from schemas.placement import PlacementQuestionOut, PlacementResultOut, PlacementSubmitIn
from services import auth_service, placement_service

router = APIRouter(prefix="/api/placement", tags=["placement"])


@router.get("/{course_slug}", response_model=list[PlacementQuestionOut])
def get_placement_questions(
    course_slug: str,
    current_user: User = Depends(auth_service.get_current_user),
):
    return placement_service.get_questions(course_slug)


@router.post("/{course_slug}/submit", response_model=PlacementResultOut)
def submit_placement(
    course_slug: str,
    payload: PlacementSubmitIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return placement_service.submit_placement(db, course_slug, current_user.id, payload)
