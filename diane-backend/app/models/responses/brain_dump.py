from pydantic import BaseModel, Field
from typing import List
from app.models.responses.task import TaskResponse
from app.models.responses.shopping_item import ShoppingItemResponse
from app.models.responses.calendar_event import CalendarEventResponse


class BrainDumpResponse(BaseModel):
    """Response after processing and saving a brain dump"""

    tasks: List[TaskResponse] = Field(default_factory=list)
    shopping_items: List[ShoppingItemResponse] = Field(default_factory=list)
    calendar_events: List[CalendarEventResponse] = Field(default_factory=list)
