import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from core.database import get_db
from models.chat_message import ChatRole
from models.user import User
from repositories import chat_repo, lesson_repo
from schemas.chat import ChatMessageIn, ChatMessageOut
from services import auth_service, ollama_service

router = APIRouter(prefix="/api/chat", tags=["ai_chat"])


@router.get("/{lesson_slug}/history", response_model=list[ChatMessageOut])
def get_history(
    lesson_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    lesson = lesson_repo.get_by_slug(db, lesson_slug)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")
    return chat_repo.get_history(db, current_user.id, lesson.id)


@router.delete("/{lesson_slug}/history")
def delete_history(
    lesson_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    lesson = lesson_repo.get_by_slug(db, lesson_slug)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")
    chat_repo.clear_history(db, current_user.id, lesson.id)
    return {"detail": "История очищена"}


@router.post("/{lesson_slug}")
async def chat(
    lesson_slug: str,
    payload: ChatMessageIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    lesson = lesson_repo.get_by_slug(db, lesson_slug)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")

    history_rows = chat_repo.get_history(db, current_user.id, lesson.id)
    history = [{"role": row.role.value, "content": row.content} for row in history_rows]

    chat_repo.add_message(db, current_user.id, lesson.id, ChatRole.user, payload.message)
    history.append({"role": "user", "content": payload.message})

    async def event_stream():
        full_reply = ""
        try:
            async for piece in ollama_service.stream_chat(lesson.title, lesson.content or "", history):
                full_reply += piece
                yield f"data: {json.dumps({'content': piece}, ensure_ascii=False)}\n\n"
        finally:
            if full_reply:
                chat_repo.add_message(db, current_user.id, lesson.id, ChatRole.assistant, full_reply)
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
