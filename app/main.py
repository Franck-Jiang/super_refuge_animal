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
from starlette.middleware.sessions import SessionMiddleware



templates = Jinja2Templates(directory="templates")
security = HTTPBearer()

app = FastAPI(
    title="Super refuge",
    description="Un super projet de super site web",
    version="0.0.1",
)

app.add_middleware(SessionMiddleware, secret_key="SecretKey")
app.include_router(router_animal)
app.include_router(router_user)

@app.get("/")
def read_root(request: Request):
    try :
        user = request.session["user"]
        role = request.session["role"]
    except:
        user = None
        role = None
    return templates.TemplateResponse("home.html", {"request": request, 
                                                    "user": user, 
                                                    "role": role})

def is_logged_in(request: Request):
    return request.session.get("user") is not None

@app.get("/add_animal")
async def add_animal_form(request: Request):
    species = session.query(AnimalSpecies).all()
    print("species queried")
    print(species)
    return templates.TemplateResponse("add_animal.html", {"request": request, "species": species})

@app.post("/query")
def query(request: Request, query: str):
    a = session.execute(text(query))
    print(a.all())
    session.commit()
    session.flush()
    
@app.get("/role")
def get_role(request: Request):
    user_logged_in = is_logged_in(request)
    print(f"{user_logged_in=}")
    return templates.TemplateResponse("index.html", {"request": request, "user_logged_in": user_logged_in})

    # _, role = user
    # if role == 1 :
    #     return templates.TemplateResponse("admin.html", {"request": request})
    # elif role == 2 :
    #     return templates.TemplateResponse("user.html", {"request": request})
    # elif role == 3 :
    #     return templates.TemplateResponse("worker.html", {"request": request})
    # else:
    #     return templates.TemplateResponse("welcome.html", {"request": request})
    