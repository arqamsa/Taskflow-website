from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.database import get_db
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def serialize(task: Task) -> TaskResponse:
    return TaskResponse.model_validate({**task.__dict__, "project_name": task.project.name if task.project else None})


def owned_task(task_id: int, user_id: int, db: Session) -> Task:
    task = db.scalar(select(Task).join(Project).where(Task.id == task_id, Project.owner_id == user_id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("", response_model=list[TaskResponse])
def list_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.scalars(select(Task).join(Project).where(Project.owner_id == user.id).order_by(Task.updated_at.desc())).all()
    return [serialize(item) for item in tasks]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.scalar(select(Project).where(Project.id == payload.project_id, Project.owner_id == user.id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return serialize(task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return serialize(owned_task(task_id, user.id, db))


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = owned_task(task_id, user.id, db)
    if payload.assigned_to is not None and db.get(User, payload.assigned_to) is None:
        raise HTTPException(status_code=404, detail="Assigned user not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return serialize(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = owned_task(task_id, user.id, db)
    db.delete(task)
    db.commit()
