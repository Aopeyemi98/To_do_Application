from pydantic import BaseModel, Field, EmailStr


class TodoRequest(BaseModel):
    title: str = Field(min_length=5)
    description: str = Field(min_length=5, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool


class UpdateTodo(TodoRequest):
    pass

    # class Config():
    #     orm_mode =  True


class UserRequest(BaseModel):
    email:EmailStr
    username: str
    first_name: str
    last_name: str
    password: str
    is_active: bool
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str