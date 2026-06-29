import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RegisterStartIn(BaseModel):
    email: EmailStr


class RegisterVerifyIn(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)


class RegisterCompleteIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=100)


class GoogleLoginIn(BaseModel):
    id_token: str


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
