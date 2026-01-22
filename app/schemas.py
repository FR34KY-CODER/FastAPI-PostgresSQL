from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List
import enum

class UserRole(str, enum.Enum):
    CLIENT = "client"
    PROVIDER = "provider"

class UserCreate(BaseModel):
    email: EmailStr
    role: UserRole

class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole
    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    title: str
    slot_time: datetime
    user_id: int

class AppointmentResponse(BaseModel):
    id: int
    title: str
    slot_time: datetime
    status: str
    user_id: int
    class Config:
        from_attributes = True