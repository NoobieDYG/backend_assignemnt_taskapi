from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")

ALGORITHM="HS256"

pwd_context=CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(password,hashed):
    return pwd_context.verify(password,hashed)

def create_token(data:dict):
    payload=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=30)
    payload["exp"]=expire
    try:
        token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
        return token
    except JWTError as e:
        print(e)
        return None
