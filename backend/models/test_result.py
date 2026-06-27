import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from core.database import Base


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.id"), nullable=False)
    score = Column(Integer, nullable=False)
    passed = Column(Boolean, nullable=False)
    mistakes = Column(JSON)
    attempt = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
