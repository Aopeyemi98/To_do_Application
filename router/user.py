from fastapi import APIRouter,Depends, HTTPException,status
from database import get_db
from sqlalchemy.orm import Session
from schema import UserRequest
from crud import user_crud


router = APIRouter(
    prefix="/users"
)


#create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, tags=["SIGN-UP"])
def create_user(request:UserRequest,db: Session=Depends(get_db)):
    new_user = user_crud.create_user(request, db)
    return new_user
 

@router.get("/", status_code=status.HTTP_200_OK, tags=["USERS"])
def get_all_user(db: Session=Depends(get_db)):
    get = user_crud.get_all_user(db)
    return get