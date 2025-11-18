"""
Pydantic models for API requests, responses, and AI processing
"""

# Request models
from app.models.requests import (
    UserLoginRequest,
    UserSignupRequest,
    BrainDumpRequest,
    TaskUpdateRequest,
    SubTaskUpdateRequest,
    ShoppingItemUpdateRequest,
    CalendarEventUpdateRequest,
)

# Response models
from app.models.responses import (
    UserResponse,
    TaskResponse,
    SubTaskResponse,
    ShoppingItemResponse,
    CalendarEventResponse,
    BrainDumpResponse,
)

# AI processing models
from app.models.ai import (
    ProcessedBrainDump,
    ProcessedTask,
    ProcessedShoppingItem,
    ProcessedCalendarEvent,
    SubTask,
)

__all__ = [
    # Requests
    "UserLoginRequest",
    "UserSignupRequest",
    "BrainDumpRequest",
    "TaskUpdateRequest",
    "SubTaskUpdateRequest",
    "ShoppingItemUpdateRequest",
    "CalendarEventUpdateRequest",
    # Responses
    "UserResponse",
    "TaskResponse",
    "SubTaskResponse",
    "ShoppingItemResponse",
    "CalendarEventResponse",
    "BrainDumpResponse",
    # AI Processing
    "ProcessedBrainDump",
    "ProcessedTask",
    "ProcessedShoppingItem",
    "ProcessedCalendarEvent",
    "SubTask",
]
