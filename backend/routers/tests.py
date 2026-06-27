from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from schemas.test_result import TestOut, TestResultOut, TestSubmitIn
from services import auth_service, test_service

router = APIRouter(tags=["tests"])


@router.get("/api/lessons/{slug}/test", response_model=TestOut)
def get_test(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return test_service.get_lesson_test(db, slug)


@router.post("/api/lessons/{slug}/test/submit", response_model=TestResultOut)
def submit_test(
    slug: str,
    payload: TestSubmitIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return test_service.submit_test(db, slug, current_user.id, payload)


@router.get("/api/lessons/{slug}/test/results", response_model=list[TestResultOut])
def get_test_results(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return test_service.get_test_results(db, slug, current_user.id)
