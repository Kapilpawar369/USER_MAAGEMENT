from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.auth.jwt.service import JWTService
from services.auth.jwt.schemas import LoginRequest, TokenResponse, RefreshRequest
from core.database.session import get_db

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    jwt_service = JWTService(db)
    return jwt_service.login(request)

@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db)):
    jwt_service = JWTService(db)
    jwt_service.logout(token)
    return {"message": "Logged out"}

@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    jwt_service = JWTService(db)
    return jwt_service.refresh_token(request)