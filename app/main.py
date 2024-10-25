from fastapi import FastAPI, Request, Form, Depends, Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer

from starlette.responses import RedirectResponse

from sqlalchemy import select, text
from models import Owner, AnimalList, AnimalRecord, User
from db import session
from auth import verify_autorization_header
from schemas.user import User as model_user

templates = Jinja2Templates(directory="templates")
security = HTTPBearer()

app = FastAPI(
    title="Super refuge",
    description="Un super projet de super site web",
    version="0.0.1",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI project!"}

@app.get("/animals")
def get_animals():
    stmt = select(AnimalList)
    res = session.execute(stmt).scalars().all()
    return res

@app.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    print(f"Username: {username}, Email: {email}, Password: {password}")
    access_token = generate_access_token(db=db, user_login=user_login)
    return RedirectResponse(url="/welcome", status_code=303)

@app.post("/signin")
def signin(request: Request, user: model_user):
    print("here")
    username = user.username
    password = user.password
    query = select(User.username, User.password).where(User.username == username, User.password == password)
    res = session.execute(query).scalars().first()
    print(res==None)
    return 200
     
@app.get("/add_animal")
async def add_animal_form(request: Request):
    species = session.query(AnimalList).all()
    print(species)
    return templates.TemplateResponse("add_animal.html", {"request": request, "species": species})

@app.get("/welcome", dependencies=[Depends(security)])
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html")

@app.post("/query")
def query(request: Request, query: str):
    a = session.execute(text(query))
    print(a.all())
    session.commit()
    session.flush()