import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    name: str
    onboarded: bool
    experienced: Optional[bool] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OnboardingIn(BaseModel):
    experienced: bool
