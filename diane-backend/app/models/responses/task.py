from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SubTaskResponse(BaseModel):
    """Subtask saved in database"""

    id: int
    parent_task_id: int
    description: str
    estimated_time_minutes: Optional[int]
    due_date: Optional[str]
    order: int
    completed: bool
    created_at: datetime


class TaskResponse(BaseModel):
    id: int
    user_id: int
    description: str
    due_date: Optional[str] = None
    estimated_time_minutes: Optional[int] = None
    completed: bool = False
    raw_input: str
    subtasks: Optional[List[SubTaskResponse]] = None
    created_at: datetime
