from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    username: str
    email : str
    password: str

class TaskCreate(BaseModel):
    title:str
    description: str

class TaskUpdate(BaseModel):
    task_id : int
    title:str