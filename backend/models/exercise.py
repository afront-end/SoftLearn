import enum
import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSON, UUID

from core.database import Base


class ExerciseType(str, enum.Enum):
    mcq = "mcq"
    open = "open"
    code = "code"


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(ExerciseType), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    options = Column(JSON)
    explanation = Column(Text)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    order = Column(Integer, default=0)
