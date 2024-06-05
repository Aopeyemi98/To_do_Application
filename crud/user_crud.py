import models
from schema import UserRequest
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from passlib.context import CryptContext


hashedPassword = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(request:UserRequest,db: Session):
    new_user = models.Users(
        email= request.email,
        username= request.username,
        first_name= request.first_name,
        last_name= request.last_name,
        hashed_password= hashedPassword.hash(request.password),
        is_active= request.is_active,
        role= request.role
    )  

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"New User successfully added"}


def get_all_user(db: Session):
    users = db.query(models.Users).all()
    return users