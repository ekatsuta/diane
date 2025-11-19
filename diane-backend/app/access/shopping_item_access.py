"""
Shopping item database access functions
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.db_models import ShoppingItem
from app.models import ShoppingItemResponse


def create_shopping_item(
    session: Session, user_id: int, description: str, raw_input: str
) -> ShoppingItemResponse:
    """Create a new shopping item"""
    shopping_item = ShoppingItem(
        user_id=user_id, description=description, raw_input=raw_input
    )
    session.add(shopping_item)
    session.flush()

    return ShoppingItemResponse.model_validate(shopping_item)


def get_shopping_items_by_user(
    session: Session, user_id: int, completed: Optional[bool] = None
) -> List[ShoppingItemResponse]:
    """Get all shopping items for a user with optional filtering"""
    query = session.query(ShoppingItem).filter(ShoppingItem.user_id == user_id)

    # Apply completed filter if provided
    if completed is not None:
        query = query.filter(ShoppingItem.completed == completed)

    items = query.all()

    return [ShoppingItemResponse.model_validate(item) for item in items]


def update_shopping_item(
    session: Session, item_id: int, update_data: Dict[str, Any]
) -> Optional[ShoppingItemResponse]:
    """Update a shopping item with provided fields"""
    item = session.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()

    if not item:
        return None

    # Update only the fields that were provided
    for field, value in update_data.items():
        if hasattr(item, field):
            setattr(item, field, value)

    session.flush()

    return ShoppingItemResponse.model_validate(item)


def delete_shopping_item(session: Session, item_id: int) -> bool:
    """Delete a shopping item"""
    item = session.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()

    if not item:
        return False

    session.delete(item)
    session.flush()
    return True
