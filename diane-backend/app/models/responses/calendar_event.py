from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date, time


class CalendarEventResponse(BaseModel):
    """Calendar event response"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    description: str
    event_date: date
    event_time: Optional[time] = None
    raw_input: str
    created_at: datetime
