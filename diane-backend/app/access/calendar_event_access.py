"""
Calendar event database access functions
"""

from typing import Optional, List, Dict, Any
from datetime import date, time, datetime
from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.db_models import CalendarEvent
from app.models import CalendarEventResponse


def create_calendar_event(
    session: Session,
    user_id: int,
    description: str,
    event_date: date,
    raw_input: str,
    event_time: Optional[time] = None,
) -> CalendarEventResponse:
    """Create a new calendar event"""
    calendar_event = CalendarEvent(
        user_id=user_id,
        description=description,
        event_date=event_date,
        event_time=event_time,
        raw_input=raw_input,
    )
    session.add(calendar_event)
    session.flush()

    return CalendarEventResponse(
        id=calendar_event.id,
        user_id=calendar_event.user_id,
        description=calendar_event.description,
        event_date=str(calendar_event.event_date),
        event_time=str(calendar_event.event_time)
        if calendar_event.event_time
        else None,
        raw_input=calendar_event.raw_input,
        created_at=calendar_event.created_at,
    )


def get_calendar_events_by_user(
    session: Session,
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[CalendarEventResponse]:
    """Get all calendar events for a user with optional date range filtering"""
    query = session.query(CalendarEvent).filter(CalendarEvent.user_id == user_id)

    # Apply date range filter if provided
    if start_date:
        query = query.filter(CalendarEvent.event_date >= start_date)
    if end_date:
        query = query.filter(CalendarEvent.event_date <= end_date)

    # Sort by event_date and event_time
    query = query.order_by(asc(CalendarEvent.event_date), asc(CalendarEvent.event_time))

    events = query.all()

    return [
        CalendarEventResponse(
            id=event.id,
            user_id=event.user_id,
            description=event.description,
            event_date=str(event.event_date),
            event_time=str(event.event_time) if event.event_time else None,
            raw_input=event.raw_input,
            created_at=event.created_at,
        )
        for event in events
    ]


def update_calendar_event(
    session: Session, event_id: int, update_data: Dict[str, Any]
) -> Optional[CalendarEventResponse]:
    """Update a calendar event with provided fields"""
    event = session.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()

    if not event:
        return None

    # Handle date conversion if event_date is in update_data
    if "event_date" in update_data and update_data["event_date"]:
        update_data["event_date"] = datetime.strptime(
            update_data["event_date"], "%Y-%m-%d"
        ).date()

    # Handle time conversion if event_time is in update_data
    if "event_time" in update_data and update_data["event_time"]:
        time_format = (
            "%H:%M:%S" if update_data["event_time"].count(":") == 2 else "%H:%M"
        )
        update_data["event_time"] = datetime.strptime(
            update_data["event_time"], time_format
        ).time()

    # Update only the fields that were provided
    for field, value in update_data.items():
        if hasattr(event, field):
            setattr(event, field, value)

    session.flush()

    return CalendarEventResponse(
        id=event.id,
        user_id=event.user_id,
        description=event.description,
        event_date=str(event.event_date),
        event_time=str(event.event_time) if event.event_time else None,
        raw_input=event.raw_input,
        created_at=event.created_at,
    )


def delete_calendar_event(session: Session, event_id: int) -> bool:
    """Delete a calendar event"""
    event = session.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()

    if not event:
        return False

    session.delete(event)
    session.flush()
    return True
