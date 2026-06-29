import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from core.database import get_db
from models.chat_message import ChatRole
from models.user import User
from repositories import assistant_repo
from schemas.assistant import AssistantMessageIn, AssistantMessageOut
from services import auth_service, ollama_service

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


@router.get("/history", response_model=list[AssistantMessageOut])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return assistant_repo.get_history(db, current_user.id)


@router.delete("/history")
def delete_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    assistant_repo.clear_history(db, current_user.id)
    return {"detail": "История очищена"}


@router.post("/")
async def chat(
    payload: AssistantMessageIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    history_rows = assistant_repo.get_history(db, current_user.id)
    history = [{"role": row.role.value, "content": row.content} for row in history_rows]

    assistant_repo.add_message(db, current_user.id, ChatRole.user, payload.message)
    history.append({"role": "user", "content": payload.message})

    async def event_stream():
        full_reply = ""
        try:
            async for piece in ollama_service.stream_platform_chat(history):
                full_reply += piece
                yield f"data: {json.dumps({'content': piece}, ensure_ascii=False)}\n\n"
        finally:
            if full_reply:
                assistant_repo.add_message(db, current_user.id, ChatRole.assistant, full_reply)
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
