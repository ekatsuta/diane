from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import ShoppingItemResponse, ShoppingItemUpdateRequest
from app.access import shopping_item_access
from app.database import get_db

router = APIRouter(prefix="/shopping-items", tags=["shopping-items"])


@router.get("/{user_id}", response_model=List[ShoppingItemResponse])
async def get_shopping_items(
    user_id: int,
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    db: Session = Depends(get_db),
):
    """Get all shopping items for a user with optional filtering"""
    try:
        items = shopping_item_access.get_shopping_items_by_user(
            session=db, user_id=user_id, completed=completed
        )
        return items
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve shopping items: {str(e)}"
        )


@router.put("/{item_id}", response_model=ShoppingItemResponse)
async def update_shopping_item(
    item_id: int,
    request: ShoppingItemUpdateRequest,
    db: Session = Depends(get_db),
):
    """Update a shopping item"""
    try:
        update_data = request.model_dump(exclude_unset=True)
        updated_item = shopping_item_access.update_shopping_item(
            session=db, item_id=item_id, update_data=update_data
        )

        if not updated_item:
            raise HTTPException(status_code=404, detail="Shopping item not found")

        db.commit()
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to update shopping item: {str(e)}"
        )


@router.delete("/{item_id}")
async def delete_shopping_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a shopping item"""
    try:
        deleted = shopping_item_access.delete_shopping_item(session=db, item_id=item_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Shopping item not found")

        db.commit()
        return {"message": "Shopping item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to delete shopping item: {str(e)}"
        )
