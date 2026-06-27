from uuid import UUID

from sqlalchemy.orm import Session

from models.lesson_chunk import LessonChunk


def delete_for_lesson(db: Session, lesson_id: UUID) -> None:
    db.query(LessonChunk).filter(LessonChunk.lesson_id == lesson_id).delete()
    db.commit()


def add_chunk(db: Session, lesson_id: UUID, chunk_index: int, content: str, embedding: list[float]) -> LessonChunk:
    chunk = LessonChunk(lesson_id=lesson_id, chunk_index=chunk_index, content=content, embedding=embedding)
    db.add(chunk)
    db.commit()
    return chunk


def search_similar(
    db: Session, query_embedding: list[float], exclude_lesson_id: UUID | None, top_k: int = 3
) -> list[LessonChunk]:
    query = db.query(LessonChunk)
    if exclude_lesson_id:
        query = query.filter(LessonChunk.lesson_id != exclude_lesson_id)
    return query.order_by(LessonChunk.embedding.cosine_distance(query_embedding)).limit(top_k).all()
