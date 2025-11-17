from pydantic import BaseModel, ConfigDict, field_serializer
from typing import Optional, List
from datetime import datetime, date


class SubTaskResponse(BaseModel):
    """Subtask saved in database"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_task_id: int
    description: str
    estimated_time_minutes: Optional[int]
    due_date: Optional[date]
    order: int
    completed: bool
    created_at: datetime


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    description: str
    due_date: Optional[date] = None
    estimated_time_minutes: Optional[int] = None
    completed: bool = False
    raw_input: str
    subtasks: Optional[List[SubTaskResponse]] = None
    created_at: datetime
