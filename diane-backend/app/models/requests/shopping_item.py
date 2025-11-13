from pydantic import BaseModel
from typing import Optional


class ShoppingItemUpdateRequest(BaseModel):
    """Request model for updating a shopping item"""

    description: Optional[str] = None
    completed: Optional[bool] = None
