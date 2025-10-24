from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate, UserUpdate
from core.common.exceptions import UserNotFoundException
from core.common.utils import hash_password, verify_password

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    # def create_user(self, user: UserCreate) -> User:
    #     password1 = hash_password(user.password)
    #     db_user = User(username=user.username, email=user.email, hashed_password=password1)
    #     self.db.add(db_user)
    #     self.db.commit()
    #     self.db.refresh(db_user)
    #     return db_user
    
    def create_user(self, user: UserCreate) -> User:
    # Check if username already exists
        existing_user = self.db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise ValueError("Username already taken")

    # Check if email already exists
        existing_email = self.db.query(User).filter(User.email == user.email).first()
        if existing_email:
            raise ValueError("Email already registered")

    # Hash the password securely
        hashed_pwd = hash_password(user.password)

    # Create and save the user
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pwd
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user


    def update_user(self, user: UserUpdate) -> User:
        db_user = self.db.query(User).filter(User.id == user.id).first()
        if not db_user:
            raise UserNotFoundException()
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete_user(self, user_id: int):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise UserNotFoundException()
        self.db.delete(db_user)
        self.db.commit()