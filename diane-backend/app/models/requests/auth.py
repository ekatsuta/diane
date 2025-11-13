from pydantic import BaseModel, EmailStr


class UserLoginRequest(BaseModel):
    """Simple email login request"""

    email: EmailStr
