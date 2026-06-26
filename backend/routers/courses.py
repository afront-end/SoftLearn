from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from repositories import course_repo
from schemas.course import CourseOut, CourseWithStacks
from services import auth_service, course_service

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return course_service.list_courses(db)


@router.get("/{slug}", response_model=CourseOut)
def get_course(slug: str, db: Session = Depends(get_db)):
    course = course_repo.get_by_slug(db, slug)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Курс не найден")
    return course


@router.get("/{slug}/stacks", response_model=CourseWithStacks)
def get_course_stacks(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return course_service.get_course_with_stacks(db, slug, current_user.id)
