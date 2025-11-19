from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ShoppingItemResponse(BaseModel):
    """Shopping item response"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    description: str
    completed: bool = False
    raw_input: str
    created_at: datetime
