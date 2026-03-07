from fastapi import FastAPI,Depends
from app.authentication import get_admin_user
from .database import engine
from fastapi.responses import HTMLResponse
from .models import Base
from . import auth_router
from . import task_router
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
Base.metadata.create_all(bind=engine)

@app.get("/",response_class=HTMLResponse)
def health_check():
    return "<h1>API is running</h1>"
@app.get("/admin")
def admin_check(user=Depends(get_admin_user)):
    return {"Message":f"Welcome admin {user['user_id']}"}
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(task_router.router, prefix="/api/v1")