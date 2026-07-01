import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    content = Column(Text)
    youtube_url = Column(String(500), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    order = Column(Integer, default=0)
    stack_id = Column(UUID(as_uuid=True), ForeignKey("stacks.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    stack = relationship("Stack", back_populates="lessons")
    exercises = relationship("Exercise", order_by="Exercise.order")
    test = relationship("Test", uselist=False)
