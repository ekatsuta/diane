"""
Test AI brain dump processing using pytest and TestClient

Brain dumps can now contain multiple categories and multiple items.
All items are automatically saved to the database.
"""

import pytest
from unittest.mock import AsyncMock, patch
from app.models import (
    ProcessedBrainDump,
    ProcessedTask,
    ProcessedShoppingItem,
    ProcessedCalendarEvent,
    SubTask,
)


@pytest.fixture
def mock_ai_service():
    """Fixture to mock the AIService"""
    with patch("app.routes.brain_dumps.ai_service") as mock:
        yield mock


def test_shopping_items_multiple(client, test_user, mock_ai_service):
    """Test processing of multiple shopping items"""
    # Mock AI response with 4 shopping items
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[],
            shopping_items=[
                ProcessedShoppingItem(description="Milk"),
                ProcessedShoppingItem(description="Eggs"),
                ProcessedShoppingItem(description="Bread"),
                ProcessedShoppingItem(description="Cheese"),
            ],
            calendar_events=[],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={
            "text": "Buy groceries: milk, eggs, bread, and cheese",
            "user_id": test_user.id,
        },
    )

    assert response.status_code == 200
    result = response.json()

    # Should return BrainDumpResponse with three lists
    assert "tasks" in result
    assert "shopping_items" in result
    assert "calendar_events" in result

    # Should have 4 shopping items
    assert len(result["shopping_items"]) == 4
    assert len(result["tasks"]) == 0
    assert len(result["calendar_events"]) == 0

    # Verify each item has database fields (saved to DB)
    for item in result["shopping_items"]:
        assert "id" in item
        assert "user_id" in item
        assert "description" in item
        assert "raw_input" in item
        assert "created_at" in item
        assert item["user_id"] == test_user.id


def test_shopping_items_simple(client, test_user, mock_ai_service):
    """Test simple shopping items"""
    # Mock AI response with 2 shopping items
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[],
            shopping_items=[
                ProcessedShoppingItem(description="Milk"),
                ProcessedShoppingItem(description="Eggs"),
            ],
            calendar_events=[],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={"text": "Need milk and eggs from the store", "user_id": test_user.id},
    )

    assert response.status_code == 200
    result = response.json()

    # Should return BrainDumpResponse
    assert "tasks" in result
    assert "shopping_items" in result
    assert "calendar_events" in result

    # Should have 2 shopping items
    assert len(result["shopping_items"]) == 2
    assert len(result["tasks"]) == 0


def test_task_simple(client, test_user, mock_ai_service):
    """Test simple task (should not be decomposed)"""
    # Mock AI response with simple task (no subtasks)
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[
                ProcessedTask(
                    description="Call the school about upcoming absence",
                    due_date=None,
                    estimated_time_minutes=10,
                    should_decompose=False,
                    reasoning="Simple phone call",
                    subtasks=[],
                )
            ],
            shopping_items=[],
            calendar_events=[],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={
            "text": "Call the school about upcoming absence",
            "user_id": test_user.id,
        },
    )

    assert response.status_code == 200
    result = response.json()

    # Should return BrainDumpResponse
    assert "tasks" in result
    assert "shopping_items" in result
    assert "calendar_events" in result

    # Should have 1 task
    assert len(result["tasks"]) == 1
    assert len(result["shopping_items"]) == 0
    assert len(result["calendar_events"]) == 0

    task = result["tasks"][0]
    # Should have database fields
    assert "id" in task
    assert "user_id" in task
    assert "description" in task
    assert "estimated_time_minutes" in task
    assert "completed" in task
    assert "raw_input" in task
    assert "created_at" in task
    assert task["user_id"] == test_user.id

    # Simple task should NOT have subtasks
    assert task["subtasks"] is None or len(task["subtasks"]) == 0


def test_task_with_due_date(client, test_user, mock_ai_service):
    """Test task with due date"""
    # Mock AI response with task that has a due date
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[
                ProcessedTask(
                    description="Buy birthday present for Noah's party",
                    due_date="2025-11-15",
                    estimated_time_minutes=30,
                    should_decompose=False,
                    reasoning="Shopping task with deadline",
                    subtasks=[],
                )
            ],
            shopping_items=[],
            calendar_events=[],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={
            "text": "Buy birthday present for Noah's party by Friday",
            "user_id": test_user.id,
        },
    )

    assert response.status_code == 200
    result = response.json()

    # Should have 1 task
    assert len(result["tasks"]) == 1

    task = result["tasks"][0]
    assert "description" in task
    assert "due_date" in task
    assert "estimated_time_minutes" in task
    assert task["user_id"] == test_user.id


def test_calendar_event_with_time(client, test_user, mock_ai_service):
    """Test calendar event with time"""
    # Mock AI response with calendar event with time
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[],
            shopping_items=[],
            calendar_events=[
                ProcessedCalendarEvent(
                    description="Doctor appointment",
                    event_date="2025-10-25",
                    event_time="14:30",
                )
            ],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={
            "text": "Doctor appointment on October 25th at 2:30pm",
            "user_id": test_user.id,
        },
    )

    assert response.status_code == 200
    result = response.json()

    # Should return BrainDumpResponse
    assert "tasks" in result
    assert "shopping_items" in result
    assert "calendar_events" in result

    # Should have 1 calendar event
    assert len(result["calendar_events"]) == 1
    assert len(result["tasks"]) == 0
    assert len(result["shopping_items"]) == 0

    event = result["calendar_events"][0]
    # Should have database fields
    assert "id" in event
    assert "user_id" in event
    assert "description" in event
    assert "event_date" in event
    assert "event_time" in event
    assert "raw_input" in event
    assert "created_at" in event
    assert event["user_id"] == test_user.id


def test_calendar_event_simple(client, test_user, mock_ai_service):
    """Test simple calendar event"""
    # Mock AI response with simple calendar event
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[],
            shopping_items=[],
            calendar_events=[
                ProcessedCalendarEvent(
                    description="Soccer practice",
                    event_date="2025-11-14",
                    event_time="16:00",
                )
            ],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={"text": "Soccer practice next Thursday at 4pm", "user_id": test_user.id},
    )

    assert response.status_code == 200
    result = response.json()

    # Should have 1 calendar event
    assert len(result["calendar_events"]) == 1
    event = result["calendar_events"][0]
    assert "description" in event
    assert "event_date" in event
    assert event["user_id"] == test_user.id


def test_shopping_items_with_quantities(client, test_user, mock_ai_service):
    """Test shopping items with quantities"""
    # Mock AI response with 3 shopping items
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[],
            shopping_items=[
                ProcessedShoppingItem(description="2 gallons of milk"),
                ProcessedShoppingItem(description="1 dozen eggs"),
                ProcessedShoppingItem(description="3 pounds of cheese"),
            ],
            calendar_events=[],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={
            "text": "Get 2 gallons of milk, 1 dozen eggs, and 3 pounds of cheese",
            "user_id": test_user.id,
        },
    )

    assert response.status_code == 200
    result = response.json()

    # Should have 3 shopping items
    assert len(result["shopping_items"]) == 3


def test_task_reminder(client, test_user, mock_ai_service):
    """Test task reminder"""
    # Mock AI response with simple task
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[
                ProcessedTask(
                    description="Call mom",
                    due_date=None,
                    estimated_time_minutes=15,
                    should_decompose=False,
                    reasoning="Simple reminder",
                    subtasks=[],
                )
            ],
            shopping_items=[],
            calendar_events=[],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={"text": "Remember to call mom this weekend", "user_id": test_user.id},
    )

    assert response.status_code == 200
    result = response.json()

    # Should have 1 task
    assert len(result["tasks"]) == 1
    task = result["tasks"][0]
    assert "description" in task
    assert "estimated_time_minutes" in task
    assert task["user_id"] == test_user.id


def test_task_complex_with_decomposition(client, test_user, mock_ai_service):
    """Test complex task that should be decomposed into subtasks"""
    # Mock AI response with complex task and subtasks
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[
                ProcessedTask(
                    description="Plan Noah's birthday party",
                    due_date=None,
                    estimated_time_minutes=180,
                    should_decompose=True,
                    reasoning="Complex event planning task",
                    subtasks=[
                        SubTask(
                            description="Create guest list",
                            order=1,
                            estimated_time_minutes=30,
                            due_date=None,
                        ),
                        SubTask(
                            description="Book venue",
                            order=2,
                            estimated_time_minutes=45,
                            due_date=None,
                        ),
                        SubTask(
                            description="Order birthday cake",
                            order=3,
                            estimated_time_minutes=20,
                            due_date=None,
                        ),
                        SubTask(
                            description="Send invitations",
                            order=4,
                            estimated_time_minutes=40,
                            due_date=None,
                        ),
                    ],
                )
            ],
            shopping_items=[],
            calendar_events=[],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={
            "text": "Plan Noah's birthday party next month",
            "user_id": test_user.id,
        },
    )

    assert response.status_code == 200
    result = response.json()

    # Should have 1 task
    assert len(result["tasks"]) == 1

    task = result["tasks"][0]
    assert "description" in task
    assert "estimated_time_minutes" in task
    assert "subtasks" in task
    assert task["user_id"] == test_user.id

    # Complex task SHOULD have subtasks
    assert task["subtasks"] is not None
    assert len(task["subtasks"]) >= 3  # Should have multiple subtasks

    # Verify subtask structure (saved to DB)
    for subtask in task["subtasks"]:
        assert "id" in subtask
        assert "parent_task_id" in subtask
        assert "description" in subtask
        assert "order" in subtask
        assert "estimated_time_minutes" in subtask
        assert "completed" in subtask
        assert "created_at" in subtask


def test_mixed_categories(client, test_user, mock_ai_service):
    """Test brain dump with multiple categories"""
    # Mock AI response with mixed categories
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[
                ProcessedTask(
                    description="Call the babysitter",
                    due_date=None,
                    estimated_time_minutes=10,
                    should_decompose=False,
                    reasoning="Simple phone call",
                    subtasks=[],
                )
            ],
            shopping_items=[
                ProcessedShoppingItem(description="Milk"),
            ],
            calendar_events=[],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={
            "text": "Call the babysitter and buy milk",
            "user_id": test_user.id,
        },
    )

    assert response.status_code == 200
    result = response.json()

    # Should return BrainDumpResponse
    assert "tasks" in result
    assert "shopping_items" in result
    assert "calendar_events" in result

    # Should have 1 task and 1 shopping item
    assert len(result["tasks"]) == 1
    assert len(result["shopping_items"]) == 1
    assert len(result["calendar_events"]) == 0

    # Verify both items are saved
    assert result["tasks"][0]["user_id"] == test_user.id
    assert result["shopping_items"][0]["user_id"] == test_user.id


def test_multiple_tasks(client, test_user, mock_ai_service):
    """Test brain dump with multiple tasks"""
    # Mock AI response with 3 tasks
    mock_ai_service.process_brain_dump = AsyncMock(
        return_value=ProcessedBrainDump(
            tasks=[
                ProcessedTask(
                    description="Call the dentist",
                    due_date=None,
                    estimated_time_minutes=10,
                    should_decompose=False,
                    reasoning="Simple phone call",
                    subtasks=[],
                ),
                ProcessedTask(
                    description="Pick up dry cleaning",
                    due_date=None,
                    estimated_time_minutes=20,
                    should_decompose=False,
                    reasoning="Quick errand",
                    subtasks=[],
                ),
                ProcessedTask(
                    description="Email the teacher",
                    due_date=None,
                    estimated_time_minutes=15,
                    should_decompose=False,
                    reasoning="Simple email",
                    subtasks=[],
                ),
            ],
            shopping_items=[],
            calendar_events=[],
        )
    )

    response = client.post(
        "/brain-dumps/",
        json={
            "text": "Call the dentist, pick up dry cleaning, and email the teacher",
            "user_id": test_user.id,
        },
    )

    assert response.status_code == 200
    result = response.json()

    # Should have 3 tasks
    assert len(result["tasks"]) == 3

    # All tasks should be saved
    for task in result["tasks"]:
        assert "id" in task
        assert "user_id" in task
        assert task["user_id"] == test_user.id
