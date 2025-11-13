from pydantic import BaseModel, Field
from typing import Optional, List


class SubTask(BaseModel):
    """A subtask created by the agent"""

    description: str
    estimated_time_minutes: Optional[int] = Field(
        None, description="Estimated time to complete in minutes"
    )
    due_date: Optional[str] = Field(None, description="Due date in YYYY-MM-DD format")
    order: int = Field(description="Order in which subtask should be completed")


class ProcessedTask(BaseModel):
    """AI-processed task data with optional decomposition"""

    description: str
    due_date: Optional[str] = None
    estimated_time_minutes: int = Field(
        description="Estimated time to complete in minutes"
    )
    should_decompose: bool = Field(
        description="Whether the task should be decomposed into subtasks"
    )
    reasoning: Optional[str] = Field(
        None, description="Agent's reasoning for decomposition decision"
    )
    subtasks: List[SubTask] = Field(
        default_factory=list, description="List of subtasks (empty if not decomposed)"
    )


class ProcessedShoppingItem(BaseModel):
    """AI-processed shopping list data"""

    description: str


class ProcessedCalendarEvent(BaseModel):
    """AI-processed calendar event data"""

    description: str
    event_date: str
    event_time: Optional[str] = None


class ProcessedBrainDump(BaseModel):
    """Result of processing a brain dump - can contain multiple categories"""

    tasks: List[ProcessedTask] = Field(
        default_factory=list, description="Tasks extracted from the brain dump"
    )
    shopping_items: List[ProcessedShoppingItem] = Field(
        default_factory=list, description="Shopping items extracted from the brain dump"
    )
    calendar_events: List[ProcessedCalendarEvent] = Field(
        default_factory=list,
        description="Calendar events extracted from the brain dump",
    )
