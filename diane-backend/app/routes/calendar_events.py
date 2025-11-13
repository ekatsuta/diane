from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models import CalendarEventResponse, CalendarEventUpdateRequest
from app.access import calendar_event_access
from app.database import get_db, get_db_transactional

router = APIRouter(prefix="/calendar-events", tags=["calendar-events"])


@router.get("/{user_id}", response_model=List[CalendarEventResponse])
async def get_calendar_events(
    user_id: int,
    start_date: Optional[date] = Query(
        None, description="Filter by start date (YYYY-MM-DD)"
    ),
    end_date: Optional[date] = Query(
        None, description="Filter by end date (YYYY-MM-DD)"
    ),
    db: Session = Depends(get_db),
):
    """Get all calendar events for a user with optional date range filtering"""
    return calendar_event_access.get_calendar_events_by_user(
        session=db, user_id=user_id, start_date=start_date, end_date=end_date
    )


@router.put("/{event_id}", response_model=CalendarEventResponse)
async def update_calendar_event(
    event_id: int,
    request: CalendarEventUpdateRequest,
    db: Session = Depends(get_db_transactional),
):
    """Update a calendar event"""
    update_data = request.model_dump(exclude_unset=True)
    updated_event = calendar_event_access.update_calendar_event(
        session=db, event_id=event_id, update_data=update_data
    )

    if not updated_event:
        raise HTTPException(status_code=404, detail="Calendar event not found")

    return updated_event


@router.delete("/{event_id}")
async def delete_calendar_event(
    event_id: int, db: Session = Depends(get_db_transactional)
):
    """Delete a calendar event"""
    deleted = calendar_event_access.delete_calendar_event(session=db, event_id=event_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Calendar event not found")

    return {"message": "Calendar event deleted successfully"}
