from datetime import date, datetime

from pydantic import BaseModel, Field

STATUS_VALUES = "^(TODO|IN_PROGRESS|REVIEW|DONE)$"
PRIORITY_VALUES = "^(LOW|MEDIUM|HIGH|CRITICAL)$"


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    description: str = Field(default="", max_length=4000)
    status: str = Field(default="TODO", pattern=STATUS_VALUES)
    priority: str = Field(default="MEDIUM", pattern=PRIORITY_VALUES)
    project_id: int
    assigned_to: int | None = None
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = Field(default=None, max_length=4000)
    status: str | None = Field(default=None, pattern=STATUS_VALUES)
    priority: str | None = Field(default=None, pattern=PRIORITY_VALUES)
    assigned_to: int | None = None
    due_date: date | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    project_id: int
    assigned_to: int | None
    due_date: date | None
    created_at: datetime
    updated_at: datetime
    project_name: str | None = None

    model_config = {"from_attributes": True}
