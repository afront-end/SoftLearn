import enum
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.database import Base


class ProgressStatus(str, enum.Enum):
    locked = "locked"
    in_progress = "in_progress"
    completed = "completed"


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    status = Column(Enum(ProgressStatus), default=ProgressStatus.locked, nullable=False)
    lesson_read = Column(Boolean, default=False)
    practice_done = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
