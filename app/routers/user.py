import hashlib
from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy import select
from sqlalchemy.orm import Session
from crud import create_user
from schemas.user import User as model_user
from db import get_db, session
from models import AnimalSpecies, User
from auth import generate_access_token


router_user = APIRouter()
templates = Jinja2Templates(directory="templates")

@router_user.get("/signup")
async def sign_up(request: Request):
    print("HTML lololol")
    return templates.TemplateResponse("signup.html", {"request": request})

@router_user.get("/signin")
def signup(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@router_user.post("/signup")
async def signup(request: Request, user = model_user):
    print(f"Username: {user.username}, Password: {user.password}")
    access_token = generate_access_token(db=session, 
                                         user_login=user)
    return RedirectResponse(url="/welcome", status_code=303)

@router_user.post("/signin")
def signin(request: Request, username: str, password: str):
    print("here")
    hashed = hashlib.sha256(password.encode()).hexdigest()
    query = select(User.username, User.password).where(User.username == username, User.password == hashed)
    res = session.execute(query).scalars().first()  
    print(res)
    return 200
     
@router_user.post("/create_user")
def create_user_route(user: model_user = Form(...), db: Session = Depends(get_db)):
    print("create_user_route")
    db_user = create_user(db=db, user=user)
    return RedirectResponse(url="/welcome", status_code=303)