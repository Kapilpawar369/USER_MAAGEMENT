from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.users.service import UserService
from services.users.schemas import UserCreate, UserUpdate, UserResponse
from core.database.session import get_db

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user)

@router.put("/update", response_model=UserResponse)
def update(user: UserUpdate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.update_user(user)

@router.delete("/delete")
def delete(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user_service.delete_user(user_id)
    return {"message": "User deleted"}