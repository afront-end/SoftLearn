from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from repositories import lesson_repo
from schemas.stack import StackOut
from schemas.lesson import StackLessonsOut
from services import auth_service, lesson_service

router = APIRouter(prefix="/api/stacks", tags=["stacks"])


@router.get("/{slug}", response_model=StackOut)
def get_stack(slug: str, db: Session = Depends(get_db)):
    stack = lesson_repo.get_stack_by_slug(db, slug)
    if not stack:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Стек не найден")
    return stack


@router.get("/{slug}/lessons", response_model=StackLessonsOut)
def get_stack_lessons(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return lesson_service.get_stack_lessons(db, slug, current_user.id)
