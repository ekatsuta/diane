from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import (
    TaskResponse,
    TaskUpdateRequest,
    SubTaskUpdateRequest,
    SubTaskResponse,
)
from app.access import task_access
from app.database import get_db, get_db_transactional

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{user_id}", response_model=List[TaskResponse])
async def get_tasks(
    user_id: int,
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    sort_by: str = Query("created_at", description="Sort by: created_at or due_date"),
    db: Session = Depends(get_db),
):
    """Get all tasks for a user with optional filtering and sorting"""
    return task_access.get_tasks_by_user(
        session=db, user_id=user_id, completed=completed, sort_by=sort_by
    )


@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a single task by ID"""
    task = task_access.get_task_by_id(session=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    db: Session = Depends(get_db_transactional),
):
    """Update a task"""
    update_data = request.model_dump(exclude_unset=True)
    updated_task = task_access.update_task(
        session=db, task_id=task_id, update_data=update_data
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db_transactional)):
    """Delete a task"""
    deleted = task_access.delete_task(session=db, task_id=task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


@router.put("/{task_id}/subtasks/{subtask_id}", response_model=SubTaskResponse)
async def update_subtask(
    task_id: int,
    subtask_id: int,
    request: SubTaskUpdateRequest,
    db: Session = Depends(get_db_transactional),
):
    """Update a subtask"""
    update_data = request.model_dump(exclude_unset=True)
    updated_subtask = task_access.update_subtask(
        session=db, subtask_id=subtask_id, update_data=update_data
    )

    if not updated_subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")

    return updated_subtask


@router.delete("/{task_id}/subtasks/{subtask_id}")
async def delete_subtask(
    task_id: int,
    subtask_id: int,
    db: Session = Depends(get_db_transactional),
):
    """Delete a subtask"""
    deleted = task_access.delete_subtask(session=db, subtask_id=subtask_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Subtask not found")

    return {"message": "Subtask deleted successfully"}
