from pydantic import BaseModel
from typing import Optional


class CalendarEventUpdateRequest(BaseModel):
    """Request model for updating a calendar event"""

    description: Optional[str] = None
    event_date: Optional[str] = None  # YYYY-MM-DD format
    event_time: Optional[str] = None  # HH:MM or HH:MM:SS format
