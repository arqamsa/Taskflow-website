from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(default="", max_length=2000)
    status: str = Field(default="ACTIVE", pattern="^(ACTIVE|ARCHIVED)$")


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    status: str | None = Field(default=None, pattern="^(ACTIVE|ARCHIVED)$")


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime
    task_count: int = 0

    model_config = {"from_attributes": True}
