from pydantic import BaseModel
from typing import Optional


class TaskUpdateRequest(BaseModel):
    """Request model for updating a task"""

    description: Optional[str] = None
    due_date: Optional[str] = None  # YYYY-MM-DD format
    estimated_time_minutes: Optional[int] = None
    completed: Optional[bool] = None


class SubTaskUpdateRequest(BaseModel):
    """Request model for updating a subtask"""

    description: Optional[str] = None
    due_date: Optional[str] = None  # YYYY-MM-DD format
    estimated_time_minutes: Optional[int] = None
    completed: Optional[bool] = None
