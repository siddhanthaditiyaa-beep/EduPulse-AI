from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Yuvraj Yadav")
    email: EmailStr = Field(..., example="yuvraj@example.com")
    password: str = Field(..., min_length=6, max_length=100, example="SecurePassword123")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="yuvraj@example.com")
    password: str = Field(..., example="SecurePassword123")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"

class StudentProfileDTO(BaseModel):
    id: int
    education_level: Optional[str] = "Undergraduate"
    learning_goal: Optional[str] = "Semester Exam Preparation"
    preferred_difficulty: Optional[str] = "medium"
    daily_study_target: Optional[int] = 45
    xp_points: Optional[int] = 0
    streak_days: Optional[int] = 1

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    profile: Optional[StudentProfileDTO] = None

    class Config:
        from_attributes = True

Token.model_rebuild()
