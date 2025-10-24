from pydantic import BaseModel
from typing import Optional
from datetime import datetime  # Added for datetime type

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None  # Updated: Use datetime type to match the model
    
    class Config:
        from_attributes = True  # Handles ORM serialization