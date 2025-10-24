from fastapi import HTTPException

class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class UserNotFoundException(CustomException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

class AuthenticationException(CustomException):
    def __init__(self):
        super().__init__(status_code=401, detail="Authentication failed")

class ValidationException(CustomException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)