"""Task management tools."""

from __future__ import annotations

from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .. import ToolExecutionError


class Task(BaseModel):
    """Simple task model stored in memory."""

    id: UUID
    project_id: UUID
    description: str
    status: str = "pending"


TASKS: Dict[UUID, Task] = {}


class CreateTaskRequest(BaseModel):
    """Input schema for creating tasks."""

    project_id: UUID = Field(...)
    description: str = Field(..., min_length=1, max_length=200)


class TaskStatusRequest(BaseModel):
    """Input schema for task status lookup."""

    task_id: UUID = Field(...)


async def create_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new task for a project."""

    data = CreateTaskRequest(**params)
    task = Task(id=uuid4(), project_id=data.project_id, description=data.description)
    TASKS[task.id] = task
    return task.model_dump(mode="json")


async def get_task_status(params: Dict[str, Any]) -> Dict[str, Any]:
    """Return status information for a task."""

    data = TaskStatusRequest(**params)
    task = TASKS.get(data.task_id)
    if not task:
        raise ToolExecutionError("task not found")
    return task.model_dump(mode="json")


TOOLS = {
    "create_task": create_task,
    "get_task_status": get_task_status,
}
