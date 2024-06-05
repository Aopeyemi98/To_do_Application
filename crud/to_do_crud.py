import models 
from sqlalchemy.orm import Session
from schema import TodoRequest, UpdateTodo
from fastapi import HTTPException, status
from router import authentication
from typing import Annotated
from fastapi import Depends


user_dependency = Annotated[dict, Depends(authentication.get_current_user)]



def add_todo(user:user_dependency, request:TodoRequest, db: Session):
    # new_todo = models.Todos(title=request.title, description=request.description, priority=request.priority, completed=request.completed)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid username")
    
    # new_todo = models.Todos(**request.model_dump(), user_id=user.get("id"))
    new_todo =  models.Todos(title=request.title, description=request.description, priority=request.priority, 
                             completed=request.completed, user_id=user.get("id"))

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return {"message":"New to_do successfully added"}
    


def read_all(db: Session):
    get = db.query(models.Todos).all()
    return get


def read_all_verified(user:user_dependency, db:Session):
    get = db.query(models.Todos).filter(models.Todos.user_id == user.get("id")).all()
    return get



def read_by_id(user: user_dependency, id, db: Session):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authentication failed")
    
    get_todo = db.query(models.Todos).filter(models.Todos.id == id)\
        .filter(models.Todos.user_id == user.get("id")).first()

    if get_todo:
        return get_todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")

    
    


def update_todo(user:user_dependency, id:int, request:UpdateTodo, db: Session):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authentication failed")
    
    todo = db.query(models.Todos).filter(models.Todos.id == id)\
    .filter(models.Todos.user_id == user.get("id")).first()

    if todo:
        todo.title = request.title
        todo.description = request.description
        todo.priority = request.priority
        todo.completed = request.completed
        # todo.update({
        #     "title": request.title,
        #     "description": request.description,
        #     "priority": request.priority,
        #     "completed":request.completed
        #     }, synchronize_session=False)
        db.add(todo)
        db.commit()
        return "To_do task successfully updated"
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found")




def delete_todo(user:user_dependency, id:int, db: Session):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authentication failed")
    
    todo = db.query(models.Todos).filter(models.Todos.id == id)\
        .filter(models.Todos.user_id == user.get("id")).first() 

    if todo:
        todo.delete(synchronize_session=False)
        db.commit()
        return "To_do task successfully deleted"
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found")