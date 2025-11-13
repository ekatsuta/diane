from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CalendarEventResponse(BaseModel):
    """Calendar event response"""

    id: int
    user_id: int
    description: str
    event_date: str
    event_time: Optional[str] = None
    raw_input: str
    created_at: datetime
