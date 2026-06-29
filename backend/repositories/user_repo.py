from sqlalchemy.orm import Session

from models.user import User


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_by_id(db: Session, user_id) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_by_google_id(db: Session, google_id: str) -> User | None:
    return db.query(User).filter(User.google_id == google_id).first()


def create(
    db: Session,
    email: str,
    password_hash: str | None,
    name: str,
    google_id: str | None = None,
) -> User:
    user = User(email=email, password_hash=password_hash, name=name, google_id=google_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
