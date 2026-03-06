from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.orm import  Session
from .database import get_db
from app.authentication import get_admin_user, get_current_user
from .models import *
from .schema import *

router=APIRouter(prefix="/tasks")

@router.post("/create")
def create_task(task:TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_task = Task(
        title=task.title,
        description=task.description,
        owner_id=user["user_id"]

    )

    db.add(new_task)

    db.commit()

    return {"message":"Task created"}

@router.get("/get")
def get_tasks(db : Session = Depends(get_db),
              user= Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.owner_id == user["user_id"]).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

@router.delete("/delete/{task_id}")
def delete_task(
    task_id: int,
    db : Session = Depends(get_db),
    user= Depends(get_admin_user)
):
    task= db.query(Task).filter(Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        db.delete(task)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting task")
    return {"message": "Task deleted"}

@router.put("/{task_id}")
def update_task(
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    task = db.query(Task).filter(Task.id == task_update.task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    try:
        task.title = task_update.title
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error updating task"
        )

    return {"message": "Task updated"}