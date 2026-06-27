import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.sql import func

from core.database import Base


class PlacementLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class PlacementTest(Base):
    __tablename__ = "placement_tests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    result_level = Column(Enum(PlacementLevel), nullable=False)
    score = Column(Integer, nullable=False)
    answers = Column(JSON, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
