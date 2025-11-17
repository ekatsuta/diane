"""
Test CRUD API endpoints for tasks, shopping items, and calendar events
"""

import pytest
from datetime import date, datetime
from app.db_models import Task, SubTask, ShoppingItem, CalendarEvent


# ==================== TEST FIXTURES ====================


@pytest.fixture
def sample_task(test_db_session, test_user):
    """Create a sample task in the database"""
    task = Task(
        user_id=test_user.id,
        description="Complete project report",
        due_date=date(2025, 12, 31),
        estimated_time_minutes=120,
        raw_input="Complete project report",
        completed=False,
    )
    test_db_session.add(task)
    test_db_session.commit()
    test_db_session.refresh(task)
    return task


@pytest.fixture
def sample_task_with_subtasks(test_db_session, test_user):
    """Create a task with subtasks"""
    task = Task(
        user_id=test_user.id,
        description="Plan vacation",
        raw_input="Plan vacation",
        completed=False,
    )
    test_db_session.add(task)
    test_db_session.flush()

    subtask1 = SubTask(
        parent_task_id=task.id,
        description="Book flights",
        order=1,
        completed=False,
    )
    subtask2 = SubTask(
        parent_task_id=task.id,
        description="Reserve hotel",
        order=2,
        completed=False,
    )
    test_db_session.add_all([subtask1, subtask2])
    test_db_session.commit()
    test_db_session.refresh(task)
    return task


@pytest.fixture
def sample_shopping_item(test_db_session, test_user):
    """Create a sample shopping item in the database"""
    item = ShoppingItem(
        user_id=test_user.id,
        description="Milk",
        raw_input="Buy milk",
        completed=False,
    )
    test_db_session.add(item)
    test_db_session.commit()
    test_db_session.refresh(item)
    return item


@pytest.fixture
def sample_calendar_event(test_db_session, test_user):
    """Create a sample calendar event in the database"""
    event = CalendarEvent(
        user_id=test_user.id,
        description="Doctor appointment",
        event_date=date(2025, 12, 15),
        event_time=datetime.strptime("14:00", "%H:%M").time(),
        raw_input="Doctor appointment on Dec 15",
    )
    test_db_session.add(event)
    test_db_session.commit()
    test_db_session.refresh(event)
    return event


# ==================== TASK TESTS ====================


def test_get_tasks_empty(client, test_user):
    """Test getting tasks when none exist"""
    response = client.get(f"/tasks/{test_user.id}")

    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_with_data(client, test_user, sample_task):
    """Test getting tasks with data"""
    # Get all tasks
    response = client.get(f"/tasks/{test_user.id}")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["user_id"] == test_user.id
    assert tasks[0]["id"] == sample_task.id
    assert "description" in tasks[0]
    assert "completed" in tasks[0]


def test_get_tasks_with_filtering(client, test_user, sample_task):
    """Test getting tasks with completed filter"""
    # Get incomplete tasks
    response = client.get(f"/tasks/{test_user.id}?completed=false")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert all(not task["completed"] for task in tasks)

    # Get completed tasks (should be empty)
    response = client.get(f"/tasks/{test_user.id}?completed=true")
    assert response.status_code == 200
    assert response.json() == []


def test_get_single_task(client, test_user, sample_task):
    """Test getting a single task by ID"""
    # Get the specific task
    response = client.get(f"/tasks/task/{sample_task.id}")

    assert response.status_code == 200
    task = response.json()
    assert task["id"] == sample_task.id
    assert task["user_id"] == test_user.id


def test_get_single_task_not_found(client):
    """Test getting a non-existent task"""
    response = client.get("/tasks/task/99999")
    assert response.status_code == 404


def test_update_task(client, test_user, sample_task):
    """Test updating a task"""
    # Update the task
    response = client.put(
        f"/tasks/{sample_task.id}",
        json={"completed": True, "description": "Complete onboarding - Updated"},
    )

    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["completed"] is True
    assert updated_task["description"] == "Complete onboarding - Updated"


def test_update_task_not_found(client):
    """Test updating a non-existent task"""
    response = client.put(
        "/tasks/99999",
        json={"completed": True},
    )
    assert response.status_code == 404


def test_delete_task(client, test_user, sample_task):
    """Test deleting a task"""
    # Delete the task
    response = client.delete(f"/tasks/{sample_task.id}")

    assert response.status_code == 200
    assert "message" in response.json()

    # Verify it's deleted
    get_response = client.get(f"/tasks/task/{sample_task.id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """Test deleting a non-existent task"""
    response = client.delete("/tasks/99999")
    assert response.status_code == 404


def test_update_subtask(client, test_user, sample_task_with_subtasks):
    """Test updating a subtask"""
    task_id = sample_task_with_subtasks.id
    subtask_id = sample_task_with_subtasks.subtasks[0].id

    # Update subtask
    response = client.put(
        f"/tasks/{task_id}/subtasks/{subtask_id}",
        json={"completed": True},
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_subtask(client, test_user, sample_task_with_subtasks):
    """Test deleting a subtask"""
    task_id = sample_task_with_subtasks.id
    subtask_id = sample_task_with_subtasks.subtasks[0].id

    # Delete subtask
    response = client.delete(f"/tasks/{task_id}/subtasks/{subtask_id}")

    assert response.status_code == 200
    assert "message" in response.json()


# ==================== SHOPPING ITEM TESTS ====================


def test_get_shopping_items_empty(client, test_user):
    """Test getting shopping items when none exist"""
    response = client.get(f"/shopping-items/{test_user.id}")

    assert response.status_code == 200
    assert response.json() == []


def test_get_shopping_items_with_data(client, test_user, sample_shopping_item):
    """Test getting shopping items with data"""
    # Get all shopping items
    response = client.get(f"/shopping-items/{test_user.id}")

    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["user_id"] == test_user.id


def test_get_shopping_items_with_filter(client, test_user, sample_shopping_item):
    """Test filtering shopping items by completion status"""
    # Get incomplete items
    response = client.get(f"/shopping-items/{test_user.id}?completed=false")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert all(not item["completed"] for item in items)


def test_update_shopping_item(client, test_user, sample_shopping_item):
    """Test updating a shopping item"""
    # Update the item
    response = client.put(
        f"/shopping-items/{sample_shopping_item.id}",
        json={"completed": True, "description": "Buy organic bananas"},
    )

    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["completed"] is True
    assert updated_item["description"] == "Buy organic bananas"


def test_update_shopping_item_not_found(client):
    """Test updating a non-existent shopping item"""
    response = client.put(
        "/shopping-items/99999",
        json={"completed": True},
    )
    assert response.status_code == 404


def test_delete_shopping_item(client, test_user, sample_shopping_item):
    """Test deleting a shopping item"""
    # Delete the item
    response = client.delete(f"/shopping-items/{sample_shopping_item.id}")

    assert response.status_code == 200
    assert "message" in response.json()


def test_delete_shopping_item_not_found(client):
    """Test deleting a non-existent shopping item"""
    response = client.delete("/shopping-items/99999")
    assert response.status_code == 404


# ==================== CALENDAR EVENT TESTS ====================


def test_get_calendar_events_empty(client, test_user):
    """Test getting calendar events when none exist"""
    response = client.get(f"/calendar-events/{test_user.id}")

    assert response.status_code == 200
    assert response.json() == []


def test_get_calendar_events_with_data(client, test_user, sample_calendar_event):
    """Test getting calendar events with data"""
    # Get all calendar events
    response = client.get(f"/calendar-events/{test_user.id}")

    assert response.status_code == 200
    events = response.json()
    assert len(events) == 1
    assert events[0]["user_id"] == test_user.id
    assert "event_date" in events[0]


def test_get_calendar_events_with_date_filter(client, test_user, sample_calendar_event):
    """Test filtering calendar events by date range"""
    # Get events with date filter
    start_date = "2025-01-01"
    end_date = "2025-12-31"
    response = client.get(
        f"/calendar-events/{test_user.id}?start_date={start_date}&end_date={end_date}"
    )

    assert response.status_code == 200
    events = response.json()
    assert len(events) == 1


def test_update_calendar_event(client, test_user, sample_calendar_event):
    """Test updating a calendar event"""
    # Update the event
    response = client.put(
        f"/calendar-events/{sample_calendar_event.id}",
        json={
            "description": "Doctor appointment - Cancelled",
            "event_date": "2025-12-20",
        },
    )

    assert response.status_code == 200
    updated_event = response.json()
    assert "Cancelled" in updated_event["description"]


def test_update_calendar_event_not_found(client):
    """Test updating a non-existent calendar event"""
    response = client.put(
        "/calendar-events/99999",
        json={"description": "Updated"},
    )
    assert response.status_code == 404


def test_delete_calendar_event(client, test_user, sample_calendar_event):
    """Test deleting a calendar event"""
    # Delete the event
    response = client.delete(f"/calendar-events/{sample_calendar_event.id}")

    assert response.status_code == 200
    assert "message" in response.json()


def test_delete_calendar_event_not_found(client):
    """Test deleting a non-existent calendar event"""
    response = client.delete("/calendar-events/99999")
    assert response.status_code == 404
