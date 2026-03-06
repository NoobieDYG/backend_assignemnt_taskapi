from sqlalchemy import *
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__="users"

    id = Column(Integer,primary_key=True)
    username= Column(String,unique=True)
    email = Column(String,unique=True)
    password= Column(String)

    role= Column(String,default="user")

class Task(Base):
    __tablename__="tasks"

    id = Column(Integer,primary_key=True)
    title= Column(String)
    description= Column(String)
    owner_id= Column(Integer,ForeignKey("users.id"))

    owner= relationship("User")