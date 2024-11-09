from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from crud import create_user
from schemas.user import User
from db import get_db, session
from models import AnimalSpecies

router_user = APIRouter(prefix="/user")
templates = Jinja2Templates(directory="templates")

@router_user.get("/sign_up")
async def sign_up(request: Request):
    print("HTML lololol")
    return templates.TemplateResponse("add_user.html", {"request": request})

@router_user.post("/create_user")
def create_user_route(user: User = Form(...), db: Session = Depends(get_db)):
    print("create_user_route")
    db_user = create_user(db=db, user=user)
    return db_user