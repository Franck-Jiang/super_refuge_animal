from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from crud import create_animal, create_species
from schemas.animal import Species, Animal
from db import get_db, session
from models import AnimalSpecies
from auth import allowed_roles

router_animal = APIRouter(prefix="/animal")
templates = Jinja2Templates(directory="templates")

@router_animal.get("/add_animal")
async def add_animal_form(request: Request):
    species = session.query(AnimalSpecies).all()
    print(species)
    return templates.TemplateResponse("add_animal.html", {"request": request, "species": species})

@router_animal.post("/create_animal")
def create_animal_route(animal: Animal = Form(...), db: Session = Depends(get_db)):
    db_user = create_animal(db=db, animal=animal)
    return db_user

@router_animal.get("/add_species", dependencies=[Depends(allowed_roles([1]))])
async def add_species_form(request: Request):
    print("router OK")
    return templates.TemplateResponse("add_species.html", {"request": request})

@router_animal.post("/create_species")
def create_species_route(species: Species = Form(...), db: Session = Depends(get_db)):
    db_user = create_species(db=db, species=species)
    return db_user