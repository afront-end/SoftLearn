import uuid
from typing import Optional

from pydantic import BaseModel


class StackOut(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: Optional[str] = None
    order: int

    class Config:
        from_attributes = True


class StackWithProgress(StackOut):
    status: str = "locked"
