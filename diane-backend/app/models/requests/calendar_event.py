from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class CalendarEventUpdateRequest(BaseModel):
    """Request model for updating a calendar event"""

    description: Optional[str] = None
    event_date: Optional[date] = None
    event_time: Optional[time] = None
