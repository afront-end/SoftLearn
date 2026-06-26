import uuid

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSON, UUID

from core.database import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), unique=True, nullable=False)
    pass_threshold = Column(Integer, default=70)
    questions = Column(JSON, nullable=False)
    time_limit = Column(Integer)
