from pydantic import BaseModel, EmailStr


class UserLoginRequest(BaseModel):
    """Simple email login request"""

    email: EmailStr


class UserSignupRequest(BaseModel):
    """User signup request with email and first name"""

    email: EmailStr
    first_name: str
