from fastapi import APIRouter,status, Depends, HTTPException,Request
from database import get_db
from schema import TodoRequest, UpdateTodo
from sqlalchemy.orm import Session
from crud import to_do_crud
from typing import List, Annotated
from . import authentication
from crud import to_do_crud
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


# Every route this is embemded with will depends on the successful vefication of this function
user_dependency = Annotated[dict, Depends(authentication.get_current_user)]



router = APIRouter(
    tags=["TO_DO\'s"],
    prefix="/to_do"
)


#testing the jinja2 connection
@router.get("/test")
async def test(request:Request):
    return templates.TemplateResponse("home.html", {"request": request})




@router.post("/", status_code=status.HTTP_201_CREATED)
def add_todo(user:user_dependency, request:TodoRequest, db: Session=Depends(get_db)):
    
    new_to_do = to_do_crud.add_todo(user,request, db)

    return new_to_do


# this route fetches all the to_do task of both verified and non-verified user
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TodoRequest])
def read_all(db: Session=Depends(get_db)):
    get = to_do_crud.read_all(db)
    return get 


# this route fetches all to_do task of a particular verified user
@router.get("/user", status_code=status.HTTP_200_OK, response_model=None)
async def read_all_verified(user:user_dependency, db: Session=Depends(get_db)):
    get_all = to_do_crud.read_all_verified(user, db)
    return get_all


#this route fetches a particular(id) to_do task of a verified user 
# @router.get("/user/{id}", status_code=status.HTTP_200_OK)
# def read_by_id(user:user_dependency, id, db: Session=Depends(get_db)):
#     get = to_do_crud.read_by_id(user, id, db)
#     return get


@router.get("/{id}", status_code=status.HTTP_200_OK)
def read_by_id(user:user_dependency, id, db: Session=Depends(get_db)):
    get = to_do_crud.read_by_id(user, id, db)
    return get



@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_todo(user:user_dependency, id:int, request:UpdateTodo, db: Session=Depends(get_db)):
    todo = to_do_crud.update_todo(user, id,request, db)
    return todo


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(user:user_dependency,id:int, db: Session=Depends(get_db)):
    todo = to_do_crud.delete_todo(user, id, db)
    return todo