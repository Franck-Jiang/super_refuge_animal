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


def welcome(request: Request, access_token: str):
    return templates.TemplateResponse("welcome.html", {"request": request, "access_token": access_token})

@router_user.get("/signup")
async def sign_up(request: Request):
    print("HTML lololol")
    return templates.TemplateResponse("signup.html", {"request": request})

@router_user.post("/signup")
def signup(request: Request,
           user: model_user = Form(...), 
           db: Session = Depends(get_db)):
    
    print(f"Username: {user.username}, Password: {user.password}")
    new_user = create_user(db=db, user=User(username=user.username, password=user.password))
    access_token = generate_access_token(db=db, 
                                        user=new_user)
    
    return welcome(request=request, access_token=access_token)


@router_user.get("/signin")
def signup(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@router_user.post("/signin")
def signin(request: Request, 
           username: str = Form(),
           password: str = Form(), 
           db: Session = Depends(get_db)):
    print("here")
    hashed = hashlib.sha256(password.encode()).hexdigest()
    query = select(User).where(User.username == username, User.password == hashed)
    res = db.execute(query).scalars().first()  
    print(res)
    access_token = generate_access_token(db=db, 
                                         user=res)
    return welcome(request=request, access_token=access_token)
