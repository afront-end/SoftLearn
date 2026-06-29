import secrets
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_db
from core.redis_client import redis_client
from models.user import User
from repositories import user_repo
from services import email_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

REGISTER_CODE_TTL_SECONDS = 600
REGISTER_VERIFIED_TTL_SECONDS = 900
GOOGLE_TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"


def _code_key(email: str) -> str:
    return f"register:code:{email.lower()}"


def _verified_key(email: str) -> str:
    return f"register:verified:{email.lower()}"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_access_token(user_id: uuid.UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def start_email_registration(db: Session, email: str) -> None:
    if not email.lower().endswith("@gmail.com"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нужен email на gmail.com")
    if user_repo.get_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже зарегистрирован")

    code = f"{secrets.randbelow(1_000_000):06d}"
    try:
        email_service.send_verification_code(email, code)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Не удалось отправить код на почту"
        ) from exc
    redis_client.set(_code_key(email), code, ex=REGISTER_CODE_TTL_SECONDS)


def verify_registration_code(email: str, code: str) -> None:
    stored_code = redis_client.get(_code_key(email))
    if not stored_code or stored_code != code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный или просроченный код")

    redis_client.delete(_code_key(email))
    redis_client.set(_verified_key(email), "1", ex=REGISTER_VERIFIED_TTL_SECONDS)


def complete_registration(db: Session, email: str, password: str, name: str) -> User:
    if not redis_client.get(_verified_key(email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email не подтверждён")
    if user_repo.get_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже зарегистрирован")

    password_hash = hash_password(password)
    user = user_repo.create(db, email=email, password_hash=password_hash, name=name)
    redis_client.delete(_verified_key(email))
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = user_repo.get_by_email(db, email)
    if not user or not user.password_hash or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")
    return user


def authenticate_google(db: Session, id_token: str) -> User:
    response = httpx.get(GOOGLE_TOKENINFO_URL, params={"id_token": id_token}, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен Google")

    payload = response.json()
    if payload.get("aud") != settings.google_client_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен Google")
    if payload.get("email_verified") not in ("true", True):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email Google не подтверждён")

    email = payload["email"]
    google_id = payload["sub"]
    name = payload.get("name") or email.split("@")[0]

    user = user_repo.get_by_google_id(db, google_id)
    if user:
        return user

    user = user_repo.get_by_email(db, email)
    if user:
        user.google_id = google_id
        db.commit()
        db.refresh(user)
        return user

    return user_repo.create(db, email=email, password_hash=None, name=name, google_id=google_id)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_repo.get_by_id(db, uuid.UUID(user_id))
    if user is None:
        raise credentials_exception
    return user
