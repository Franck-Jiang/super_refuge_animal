from fastapi import FastAPI, Request, Form, Depends, Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer

from sqlalchemy import select, text
from models import Owner, AnimalSpecies, AnimalRecord, User
from db import session
from auth import verify_autorization_header, generate_access_token, get_current_user
from schemas.user import User as model_user
from routers.animal import router_animal
from routers.user import router_user


templates = Jinja2Templates(directory="templates")
security = HTTPBearer()

app = FastAPI(
    title="Super refuge",
    description="Un super projet de super site web",
    version="0.0.1",
)

app.include_router(router_animal)
app.include_router(router_user)

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/animals")
def get_animals():
    stmt = select(AnimalSpecies)
    res = session.execute(stmt).scalars().all()
    return res


@app.get("/add_animal")
async def add_animal_form(request: Request):
    species = session.query(AnimalSpecies).all()
    print("species queried")
    print(species)
    return templates.TemplateResponse("add_animal.html", {"request": request, "species": species})

@app.get("/welcome", dependencies=[Depends(security)])
def welcome(request: Request, access_token: str):
    return templates.TemplateResponse("welcome.html", {"request": request, "access_token": access_token})

@app.post("/query")
def query(request: Request, query: str):
    a = session.execute(text(query))
    print(a.all())
    session.commit()
    session.flush()
    
@app.get("/role")
def get_role(request: Request, user: User = Depends(get_current_user)):
    print(f"{user=}")
    _, role = user
    if role == 1 :
        return templates.TemplateResponse("admin.html", {"request": request})
    elif role == 2 :
        return templates.TemplateResponse("user.html", {"request": request})
    elif role == 3 :
        return templates.TemplateResponse("worker.html", {"request": request})
    else:
        return templates.TemplateResponse("welcome.html", {"request": request})
    