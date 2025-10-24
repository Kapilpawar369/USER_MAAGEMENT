import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")  # Updated: Use PBKDF2-SHA256 instead of bcrypt to avoid compatibility issues

def hash_password(password: str) -> str:
    return pwd_context.hash(password)  # No truncation needed for PBKDF2

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

class GeneralUtils:
    @staticmethod
    def generate_id() -> str:
        return hashlib.md5(str(id).encode()).hexdigest()