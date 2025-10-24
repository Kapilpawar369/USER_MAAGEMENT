from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .schemas import LoginRequest, TokenResponse, RefreshRequest, TokenData
from services.users.models import User
from core.config import settings
from core.common.exceptions import AuthenticationException
from core.common.utils import verify_password

class JWTService:
    def __init__(self, db: Session):
        self.db = db
    
    def login(self, request: LoginRequest) -> TokenResponse:
        user = self.db.query(User).filter(User.username == request.username).first()
        if not user or not verify_password(request.password, user.hashed_password):
            raise AuthenticationException()
        access_token = self._create_access_token({"sub": user.username})
        refresh_token = self._create_refresh_token({"sub": user.username})
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    def logout(self, token: str):
        # Implement token blacklisting if needed
        pass
    
    def refresh_token(self, request: RefreshRequest) -> TokenResponse:
        try:
            payload = jwt.decode(request.refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            username = payload.get("sub")
            if not username:
                raise AuthenticationException()
            access_token = self._create_access_token({"sub": username})
            return TokenResponse(access_token=access_token, refresh_token=request.refresh_token)
        except JWTError:
            raise AuthenticationException()
    
    def _create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    def _create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)