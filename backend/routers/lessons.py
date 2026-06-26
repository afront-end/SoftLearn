from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from schemas.lesson import LessonDetail
from services import auth_service, lesson_service

router = APIRouter(prefix="/api/lessons", tags=["lessons"])


@router.get("/{slug}", response_model=LessonDetail)
def get_lesson(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return lesson_service.get_lesson_detail(db, slug, current_user.id)


@router.patch("/{slug}/read", response_model=LessonDetail)
def mark_lesson_read(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return lesson_service.mark_lesson_read(db, slug, current_user.id)
