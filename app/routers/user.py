import hashlib
from fastapi import APIRouter, Depends, Request, Form, HTTPException
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

@router_user.post("/signup")
def signup(request: Request,
           user: model_user = Form(...), 
           db: Session = Depends(get_db)):
    
    print(f"Username: {user.username}, Password: {user.password}")
    try :
        new_user = create_user(db=db, user=User(username=user.username, password=user.password))
    except HTTPException as e:
        print(f"Error while creating user: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=f"User creation failed: {e.detail}")

    access_token = generate_access_token(db=db, 
                                        user=new_user)
    request.session["user"] = new_user.username
    request.session["role"] = new_user.category_id
    return templates.TemplateResponse("welcome.html", {"request": request, 
                                                       "access_token": access_token, 
                                                       "user": new_user.username})


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
    if res:
        print(res)
        request.session["user"] = res.username
        request.session["role"] = res.category_id
        access_token = generate_access_token(db=db, 
                                            user=res)
        return templates.TemplateResponse("welcome.html", {"request": request, 
                                                           "access_token": access_token, 
                                                           "user": res.username})
    else:
        return templates.TemplateResponse("signin.html", {"request": request, "error_message": "Invalid username or password"})
    

@router_user.get("/logout")
def logout(request: Request):
    request.session.clear() 
    return RedirectResponse(url="/", status_code=303)

@router_user.get("/add_worker")
def add_worker(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.category_id==2).all()
    api_action = "/add_worker"
    return templates.TemplateResponse("add_worker.html", {"request": request, "users": users, "api_action": api_action})
    
@router_user.post("/add_worker")
def add_worker_post(request: Request, user_id: int = Form(...), db: Session = Depends(get_db)):
    # Find the user based on the user_id from the form
    selected_user = db.query(User).filter(User.id==user_id).first()
    if selected_user:
        if selected_user.category_id == 2:
            selected_user.category_id = 3
            db.commit()
            return {"message": f"Selected worker: {selected_user.username}, ID: {selected_user.id}, category_id changed to {selected_user.category_id}"}
        else:
            return {"error": "User's category_id is not 'User', so it cannot be updated to 'Worker'"}
    else:
        return {"error": "User not found"}
    
@router_user.get("/remove_worker")
def add_worker(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.category_id==3).all()
    api_action = "/remove_worker"
    return templates.TemplateResponse("add_worker.html", {"request": request, "users": users, "api_action": api_action})

@router_user.post("/remove_worker")
def add_worker_post(request: Request, user_id: int = Form(...), db: Session = Depends(get_db)):
    # Find the user based on the user_id from the form
    selected_user = db.query(User).filter(User.id==user_id).first()
    if selected_user:
        if selected_user.category_id == 3:
            selected_user.category_id = 2
            db.commit()
            return {"message": f"Selected worker: {selected_user.username}, ID: {selected_user.id}, category_id changed to {selected_user.category_id}"}
        else:
            return {"error": "User's category_id is not 'Worker', so it cannot be updated to 'User'"}
    else:
        return {"error": "User not found"}
    
@router_user.get("/remove_user")
def add_worker(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.category_id==2).all()
    api_action = "/remove_user"
    return templates.TemplateResponse("add_worker.html", {"request": request, "users": users, "api_action": api_action})

@router_user.post("/remove_user")
def add_worker_post(request: Request, user_id: int = Form(...), db: Session = Depends(get_db)):
    # Find the user based on the user_id from the form
    selected_user = db.query(User).filter(User.id==user_id).first()
    if selected_user:
        if selected_user.category_id == 2:
            db.delete(selected_user)
            db.commit()
            return {"message": f"Selected worker: {selected_user.username}, ID: {selected_user.id}, removed"}
        else:
            return {"error": "User's category_id is not 'User', so it cannot be removed"}
    else:
        return {"error": "User not found"}