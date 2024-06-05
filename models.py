from database import Base
from sqlalchemy import String, Integer, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship




class Users(Base): #user table
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, unique= True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    # to_do_list = relationship("Todos", back_populates="creator")



class Todos(Base): #Table for things to_do
    __tablename__ = "todos"

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String(50), nullable= False)
    description = Column(String(100), nullable = False)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # creator = relationship("User", back_populates="to_do_list")
    


