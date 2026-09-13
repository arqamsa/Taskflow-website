from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_projects: int
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    tasks_by_status: dict[str, int]
    tasks_by_priority: dict[str, int]
    recent_tasks: list[dict]
