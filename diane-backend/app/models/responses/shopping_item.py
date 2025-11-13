from pydantic import BaseModel
from datetime import datetime


class ShoppingItemResponse(BaseModel):
    """Shopping item response"""

    id: int
    user_id: int
    description: str
    completed: bool = False
    raw_input: str
    created_at: datetime
