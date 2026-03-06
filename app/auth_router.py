from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .auth import *
from .models import *
from .schema import *

router=APIRouter(prefix="/auth")

@router.post("/register")
def register(user: UserRegister, db: Session= Depends(get_db)):
    existing=db.query(User).filter(User.email==user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed= hash_password(user.password)

    new_user= User(
        username=user.username,
        email=user.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    return {"Message":"User registered successfully"}

@router.post("/login")
def login(user:UserLogin, db: Session= Depends(get_db)):
    db_user= db.query(User).filter(User.email==user.email).first()
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token= create_token({
        "user_id":db_user.id,
        "role":db_user.role
    })
    return {'access_token': token,
            'token_type': 'bearer'}


    
