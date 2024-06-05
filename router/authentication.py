from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
import models
from crud import user_crud
from jose import jwt, JWTError
from datetime import timedelta,datetime
from schema import Token

router = APIRouter(
    tags=["AUTHENTICATION"],
    prefix="/Login"
)

SECRET_KEY = "secret" # openssl rand -hex 32(to form a secret key that cant be easily forged)
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="Login")





def authenticate_user(username:str, password:str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid username")
    
    if not user_crud.hashedPassword.verify(password, user.hashed_password):
        return False
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid password")
    
    return user


def create_access_token(username:str, user_id:int, expires_delta:timedelta):
    encode = {"sub":username, "id":user_id,}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


# Other routes on the app will depends on this function after the access_token has been generated
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail= "Invalid authentication")
        return {"username":username, "id":user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= "Invalid Authentication")
    



@router.post("/", response_model=Token)
async def login_for_access_code(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db)):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        # return "failed authentication"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= "Failed Authentication..Invalid Username or Password")
    
    token = create_access_token(user.username, user.id, timedelta(minutes=10))

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# pip install "python-jose[cryptography]" for token