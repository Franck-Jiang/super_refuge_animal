from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy import select
from sqlalchemy.orm import Session
from crud import create_animal, create_species
from schemas.animal import Species, Animal
from db import get_db, session
from models import AnimalSpecies, AnimalRecord, Adoption, User
from auth import allowed_roles
from datetime import datetime

router_animal = APIRouter(prefix="/animal")
templates = Jinja2Templates(directory="templates")

# ================== No authentication needed ================== #
@router_animal.get("/show")
def show_animals(request: Request, db: Session = Depends(get_db)):
    animals = (db.query(AnimalRecord, AnimalSpecies.species_name)
               .join(AnimalSpecies, AnimalRecord.animal_id == AnimalSpecies.id)
               .filter(AnimalRecord.adopted == False)
               .all())
    species = db.query(AnimalSpecies.species_name).all()
    # print(animals)
    # for a in animals:
    #     print(a[0].name)
    
    if not animals or not species:
        request.session["flash_message"] = f"No animals in the database ! Ask admin"
        return RedirectResponse("/", status_code=200)
    
    return templates.TemplateResponse("show_animals.html", {"request": request, "animals": animals, "species": species})


# ================== User/Worker/Admin  ================== #
@router_animal.get("/adopt", dependencies=[Depends(allowed_roles([1, 2, 3]))])
def get_adopt(request: Request, db: Session = Depends(get_db)):
    animals_record = db.query(AnimalRecord).all()
    if not animals_record:
        request.session["flash_message"] = f"No animals in the database ! Ask admin"
        return RedirectResponse("/", status_code=200)
    
    return templates.TemplateResponse("adoption.html", {"request": request, "animals_record": animals_record})

@router_animal.post("/adopt", dependencies=[Depends(allowed_roles([1, 2, 3]))])
def post_adopt(request: Request, animal_id: int = Form(...), db: Session = Depends(get_db)):
    try:
        user = request.session["user"]
        user_id = db.query(User).filter(User.username == user).first().id
        # print(f"{user_id=}")
    except KeyError:
        raise HTTPException(status_code=403, detail="Not logged in")

    selected_animal = db.query(AnimalRecord).filter(AnimalRecord.id == animal_id).first()
    if not selected_animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    new_adoption = Adoption(animal_id=selected_animal.id, 
                            user_adopter_id=user_id,
                            validated=False)
    db.add(new_adoption)
    db.commit()

    request.session["flash_message"] = f"Adoption of {selected_animal.name} acknowledged !"

    return RedirectResponse("/", status_code=303)

# ================== Worker/Admin  ================== #
@router_animal.get("/valid_adopt", dependencies=[Depends(allowed_roles([1, 3]))])
def get_validation(request: Request, db: Session = Depends(get_db)):
    adoption_list = (db.query(Adoption, User, AnimalRecord)
                     .join(User, Adoption.user_adopter_id == User.id)
                     .join(AnimalRecord, Adoption.animal_id == AnimalRecord.id).all())
    # print(adoption_list)
    return templates.TemplateResponse("validation.html", {"request": request, "adoption_list": adoption_list})

@router_animal.post("/valid_adopt", dependencies=[Depends(allowed_roles([1, 3]))])
def post_validation(request: Request, db: Session = Depends(get_db), adoption_id: int = Form(...)):
    adoption = db.query(Adoption).filter(Adoption.id == adoption_id).first()
    if not adoption:
        HTTPException(status_code=404, detail="Adoption not found")
        
    adoption.adoption_date = datetime.now()  
    adoption.validated = True
    
        
    animal = db.query(AnimalRecord).filter(AnimalRecord.id == adoption.animal_id).first()
    if not animal:
        HTTPException(status_code=404, detail="Animal not found")
    animal.adopted = True
        
    db.commit()
    db.refresh(adoption)  
    db.refresh(animal)  
    request.session["flash_message"] = f"Adoption n° {adoption.id} validated !"
    
    return RedirectResponse("/", status_code=303)

@router_animal.get("/add_animal", dependencies=[Depends(allowed_roles([1, 3]))])
def add_animal_form(request: Request):
    species = session.query(AnimalSpecies).all()
    # print(species)
    if not species:
        request.session["flash_message"] = f"No species in the database ! Ask admin"
        return RedirectResponse("/", status_code=200)
    return templates.TemplateResponse("add_animal.html", {"request": request, "species": species})

@router_animal.post("/create_animal", dependencies=[Depends(allowed_roles([1, 3]))])
def create_animal_route(animal: Animal = Form(...), db: Session = Depends(get_db)):
    db_user = create_animal(db=db, animal=animal)
    return db_user
# ================== Admin  ================== #

@router_animal.get("/add_species", dependencies=[Depends(allowed_roles([1]))])
def add_species_form(request: Request):
    # print("router OK")
    api_action = "/animal/create_species"
    return templates.TemplateResponse("add_species.html", {"request": request, 
                                                           "api_action": api_action})

@router_animal.post("/create_species", dependencies=[Depends(allowed_roles([1]))])
def create_species_route(species: Species = Form(...), db: Session = Depends(get_db)):
    db_user = create_species(db=db, species=species)
    return db_user


@router_animal.get("/remove_species", dependencies=[Depends(allowed_roles([1]))])
def add_species_form(request: Request):
    # print("router OK")
    api_action = "/animal/remove_species"
    return templates.TemplateResponse("add_species.html", {"request": request, 
                                                           "api_action": api_action})

@router_animal.post("/remove_species", dependencies=[Depends(allowed_roles([1]))])
def create_species_route(species: Species = Form(...), db: Session = Depends(get_db)):
    selected_species = db.query(AnimalSpecies).filter(AnimalSpecies.species_name==species.specie_name).first()

    if selected_species:
        db.delete(selected_species)
        db.commit()
        return {"message": f"Selected species: {selected_species.species_name}, ID: {selected_species.id}, removed"}
    else:
        return {"error": "Species not found"}
    
