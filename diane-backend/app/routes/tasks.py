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
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{user_id}", response_model=List[TaskResponse])
async def get_tasks(
    user_id: int,
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    sort_by: str = Query("created_at", description="Sort by: created_at or due_date"),
    db: Session = Depends(get_db),
):
    """Get all tasks for a user with optional filtering and sorting"""
    try:
        tasks = task_access.get_tasks_by_user(
            session=db, user_id=user_id, completed=completed, sort_by=sort_by
        )
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve tasks: {str(e)}"
        )


@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a single task by ID"""
    try:
        task = task_access.get_task_by_id(session=db, task_id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve task: {str(e)}"
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    db: Session = Depends(get_db),
):
    """Update a task"""
    try:
        update_data = request.model_dump(exclude_unset=True)
        updated_task = task_access.update_task(
            session=db, task_id=task_id, update_data=update_data
        )

        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")

        db.commit()
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    try:
        deleted = task_access.delete_task(session=db, task_id=task_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")

        db.commit()
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")


@router.put("/{task_id}/subtasks/{subtask_id}", response_model=SubTaskResponse)
async def update_subtask(
    task_id: int,
    subtask_id: int,
    request: SubTaskUpdateRequest,
    db: Session = Depends(get_db),
):
    """Update a subtask"""
    try:
        update_data = request.model_dump(exclude_unset=True)
        updated_subtask = task_access.update_subtask(
            session=db, subtask_id=subtask_id, update_data=update_data
        )

        if not updated_subtask:
            raise HTTPException(status_code=404, detail="Subtask not found")

        db.commit()
        return updated_subtask
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to update subtask: {str(e)}"
        )


@router.delete("/{task_id}/subtasks/{subtask_id}")
async def delete_subtask(
    task_id: int,
    subtask_id: int,
    db: Session = Depends(get_db),
):
    """Delete a subtask"""
    try:
        deleted = task_access.delete_subtask(session=db, subtask_id=subtask_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Subtask not found")

        db.commit()
        return {"message": "Subtask deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to delete subtask: {str(e)}"
        )
