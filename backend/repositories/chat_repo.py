from uuid import UUID

from sqlalchemy.orm import Session

from models.chat_message import ChatMessage, ChatRole


def get_history(db: Session, user_id: UUID, lesson_id: UUID) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id, ChatMessage.lesson_id == lesson_id)
        .order_by(ChatMessage.created_at)
        .all()
    )


def add_message(db: Session, user_id: UUID, lesson_id: UUID, role: ChatRole, content: str) -> ChatMessage:
    message = ChatMessage(user_id=user_id, lesson_id=lesson_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def clear_history(db: Session, user_id: UUID, lesson_id: UUID) -> None:
    db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id, ChatMessage.lesson_id == lesson_id
    ).delete()
    db.commit()
