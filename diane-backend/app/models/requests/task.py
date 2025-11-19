from pydantic import BaseModel
from typing import Optional
from datetime import date


class TaskUpdateRequest(BaseModel):
    """Request model for updating a task"""

    description: Optional[str] = None
    due_date: Optional[date] = None
    estimated_time_minutes: Optional[int] = None
    completed: Optional[bool] = None


class SubTaskUpdateRequest(BaseModel):
    """Request model for updating a subtask"""

    description: Optional[str] = None
    due_date: Optional[date] = None
    estimated_time_minutes: Optional[int] = None
    completed: Optional[bool] = None
