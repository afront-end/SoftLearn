from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from schemas.user import OnboardingIn, UserOut
from services import auth_service

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])


@router.post("", response_model=UserOut)
def complete_onboarding(
    payload: OnboardingIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    current_user.onboarded = True
    current_user.experienced = payload.experienced
    db.commit()
    db.refresh(current_user)
    return current_user
