import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database import Base

EMBEDDING_DIM = 768


class LessonChunk(Base):
    __tablename__ = "lesson_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(EMBEDDING_DIM), nullable=False)

    lesson = relationship("Lesson")
