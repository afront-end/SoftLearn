from uuid import UUID

from sqlalchemy.orm import Session

from models.lesson import Lesson
from repositories import lesson_chunk_repo
from services import ollama_service


def chunk_content(content: str, max_chars: int = 600) -> list[str]:
    """Делит markdown урока на чанки по заголовкам ## , дробя длинные секции."""
    if not content:
        return []

    sections = []
    current = ""
    for line in content.split("\n"):
        if line.startswith("## ") and current.strip():
            sections.append(current.strip())
            current = ""
        current += line + "\n"
    if current.strip():
        sections.append(current.strip())

    chunks: list[str] = []
    for section in sections:
        if len(section) <= max_chars:
            chunks.append(section)
            continue
        words = section.split()
        buf = ""
        for word in words:
            if len(buf) + len(word) + 1 > max_chars:
                chunks.append(buf.strip())
                buf = ""
            buf += word + " "
        if buf.strip():
            chunks.append(buf.strip())

    return chunks


async def index_lesson(db: Session, lesson: Lesson) -> int:
    lesson_chunk_repo.delete_for_lesson(db, lesson.id)
    chunks = chunk_content(lesson.content or "")
    for i, chunk in enumerate(chunks):
        embedding = await ollama_service.embed_text(chunk)
        lesson_chunk_repo.add_chunk(db, lesson.id, i, chunk, embedding)
    return len(chunks)


async def retrieve_context(db: Session, query_text: str, exclude_lesson_id: UUID, top_k: int = 3) -> list[str]:
    query_embedding = await ollama_service.embed_text(query_text)
    chunks = lesson_chunk_repo.search_similar(db, query_embedding, exclude_lesson_id, top_k)
    return [f"[{c.lesson.title}]\n{c.content}" for c in chunks]
