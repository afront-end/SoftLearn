from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from schemas.progress import ProgressOverviewOut, StackProgressEntryOut
from services import auth_service, progress_service

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("", response_model=ProgressOverviewOut)
def get_progress_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return progress_service.get_overview(db, current_user.id)


@router.get("/stacks", response_model=list[StackProgressEntryOut])
def get_progress_stacks(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return progress_service.get_stack_progress_list(db, current_user.id)
