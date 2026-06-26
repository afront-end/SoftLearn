import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base
from models.progress import ProgressStatus


class StackProgress(Base):
    __tablename__ = "stack_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    stack_id = Column(UUID(as_uuid=True), ForeignKey("stacks.id"), nullable=False)
    status = Column(Enum(ProgressStatus), default=ProgressStatus.locked, nullable=False)
    unlocked_at = Column(DateTime(timezone=True))
