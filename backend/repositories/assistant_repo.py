from uuid import UUID

from sqlalchemy.orm import Session

from models.assistant_message import AssistantMessage
from models.chat_message import ChatRole


def get_history(db: Session, user_id: UUID) -> list[AssistantMessage]:
    return (
        db.query(AssistantMessage)
        .filter(AssistantMessage.user_id == user_id)
        .order_by(AssistantMessage.created_at)
        .all()
    )


def add_message(db: Session, user_id: UUID, role: ChatRole, content: str) -> AssistantMessage:
    message = AssistantMessage(user_id=user_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def clear_history(db: Session, user_id: UUID) -> None:
    db.query(AssistantMessage).filter(AssistantMessage.user_id == user_id).delete()
    db.commit()
