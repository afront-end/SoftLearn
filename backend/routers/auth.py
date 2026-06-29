from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from schemas.user import (
    GoogleLoginIn,
    RegisterCompleteIn,
    RegisterStartIn,
    RegisterVerifyIn,
    Token,
    UserLogin,
    UserOut,
)
from services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register/start")
def register_start(payload: RegisterStartIn, db: Session = Depends(get_db)):
    auth_service.start_email_registration(db, payload.email)
    return {"detail": "Код отправлен на почту"}


@router.post("/register/verify")
def register_verify(payload: RegisterVerifyIn):
    auth_service.verify_registration_code(payload.email, payload.code)
    return {"detail": "Email подтверждён"}


@router.post("/register/complete", response_model=Token)
def register_complete(payload: RegisterCompleteIn, db: Session = Depends(get_db)):
    user = auth_service.complete_registration(db, payload.email, payload.password, payload.name)
    token = auth_service.create_access_token(user.id)
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    token = auth_service.create_access_token(user.id)
    return Token(access_token=token)


@router.post("/google", response_model=Token)
def google_login(payload: GoogleLoginIn, db: Session = Depends(get_db)):
    user = auth_service.authenticate_google(db, payload.id_token)
    token = auth_service.create_access_token(user.id)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.post("/logout")
def logout():
    return {"detail": "Выход выполнен"}
