"""
Task database access functions
"""

from typing import Optional, List, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.db_models import Task, SubTask
from app.models import TaskResponse, SubTaskResponse


def create_task(
    session: Session,
    user_id: int,
    description: str,
    raw_input: str,
    due_date: Optional[date] = None,
    estimated_time_minutes: Optional[int] = None,
) -> TaskResponse:
    """Create a new task"""
    task = Task(
        user_id=user_id,
        description=description,
        due_date=due_date,
        estimated_time_minutes=estimated_time_minutes,
        raw_input=raw_input,
    )
    session.add(task)
    session.flush()

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        description=task.description,
        due_date=str(task.due_date) if task.due_date else None,
        estimated_time_minutes=task.estimated_time_minutes,
        completed=task.completed,
        raw_input=task.raw_input,
        subtasks=None,
        created_at=task.created_at,
    )


def create_subtasks(
    session: Session,
    parent_task_id: int,
    subtasks: List[dict],
) -> List[SubTaskResponse]:
    """Create multiple subtasks for a parent task"""
    subtask_objects = [
        SubTask(
            parent_task_id=parent_task_id,
            description=subtask_data["description"],
            order=subtask_data["order"],
            estimated_time_minutes=subtask_data.get("estimated_time_minutes"),
            due_date=subtask_data.get("due_date"),
        )
        for subtask_data in subtasks
    ]

    session.add_all(subtask_objects)
    session.flush()

    # Convert to response models
    # TODO: use pydantic's model_validate
    return [
        SubTaskResponse(
            id=subtask.id,
            parent_task_id=subtask.parent_task_id,
            description=subtask.description,
            order=subtask.order,
            estimated_time_minutes=subtask.estimated_time_minutes,
            due_date=str(subtask.due_date) if subtask.due_date else None,
            completed=subtask.completed,
            created_at=subtask.created_at,
        )
        for subtask in subtask_objects
    ]


def _task_to_response(task: Task) -> TaskResponse:
    """Helper function to convert Task ORM model to TaskResponse"""
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        description=task.description,
        due_date=str(task.due_date) if task.due_date else None,
        estimated_time_minutes=task.estimated_time_minutes,
        completed=task.completed,
        raw_input=task.raw_input,
        subtasks=[
            SubTaskResponse(
                id=st.id,
                parent_task_id=st.parent_task_id,
                description=st.description,
                order=st.order,
                estimated_time_minutes=st.estimated_time_minutes,
                due_date=str(st.due_date) if st.due_date else None,
                completed=st.completed,
                created_at=st.created_at,
            )
            for st in task.subtasks
        ],
        created_at=task.created_at,
    )


def get_tasks_by_user(
    session: Session,
    user_id: int,
    completed: Optional[bool] = None,
    sort_by: str = "created_at",
) -> List[TaskResponse]:
    """Get all tasks for a user with optional filtering and sorting"""
    query = session.query(Task).filter(Task.user_id == user_id)

    # Apply completed filter if provided
    if completed is not None:
        query = query.filter(Task.completed == completed)

    # Apply sorting
    if sort_by == "due_date":
        query = query.order_by(asc(Task.due_date))
    elif sort_by == "created_at":
        query = query.order_by(desc(Task.created_at))

    tasks = query.all()
    return [_task_to_response(task) for task in tasks]


def get_task_by_id(session: Session, task_id: int) -> Optional[TaskResponse]:
    """Get a single task by ID with its subtasks"""
    task = session.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    return _task_to_response(task)


def update_task(
    session: Session, task_id: int, update_data: Dict[str, Any]
) -> Optional[TaskResponse]:
    """Update a task with provided fields"""
    task = session.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    # Handle date conversion if due_date is in update_data
    if "due_date" in update_data and update_data["due_date"]:
        update_data["due_date"] = datetime.strptime(
            update_data["due_date"], "%Y-%m-%d"
        ).date()

    # Update only the fields that were provided
    for field, value in update_data.items():
        if hasattr(task, field):
            setattr(task, field, value)

    session.flush()
    return _task_to_response(task)


def delete_task(session: Session, task_id: int) -> bool:
    """Delete a task (subtasks will be cascade deleted)"""
    task = session.query(Task).filter(Task.id == task_id).first()

    if not task:
        return False

    session.delete(task)
    session.flush()
    return True


def update_subtask(
    session: Session, subtask_id: int, update_data: Dict[str, Any]
) -> Optional[SubTaskResponse]:
    """Update a subtask with provided fields"""
    subtask = session.query(SubTask).filter(SubTask.id == subtask_id).first()

    if not subtask:
        return None

    # Handle date conversion if due_date is in update_data
    if "due_date" in update_data and update_data["due_date"]:
        update_data["due_date"] = datetime.strptime(
            update_data["due_date"], "%Y-%m-%d"
        ).date()

    # Update only the fields that were provided
    for field, value in update_data.items():
        if hasattr(subtask, field):
            setattr(subtask, field, value)

    session.flush()

    return SubTaskResponse(
        id=subtask.id,
        parent_task_id=subtask.parent_task_id,
        description=subtask.description,
        order=subtask.order,
        estimated_time_minutes=subtask.estimated_time_minutes,
        due_date=str(subtask.due_date) if subtask.due_date else None,
        completed=subtask.completed,
        created_at=subtask.created_at,
    )


def delete_subtask(session: Session, subtask_id: int) -> bool:
    """Delete a subtask"""
    subtask = session.query(SubTask).filter(SubTask.id == subtask_id).first()

    if not subtask:
        return False

    session.delete(subtask)
    session.flush()
    return True
