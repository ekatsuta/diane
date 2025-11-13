from pydantic import BaseModel


class UserResponse(BaseModel):
    """User response"""

    id: int
    email: str
    first_name: str
