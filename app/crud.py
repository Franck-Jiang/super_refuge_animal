from sqlalchemy.orm import Session
from schemas.animal import Species, Animal
from schemas.user import User as User_schema
from models import AnimalSpecies, AnimalRecord, User
from datetime import datetime
import hashlib
from fastapi import HTTPException


def create_species(db: Session, specie: Species, ) -> AnimalSpecies:
    db_specie = AnimalSpecies(specie_name  =specie.specie_name,
                              food         =specie.food)
    db.add(db_specie)
    db.commit()
    db.refresh(db_specie)
    return db_specie

def create_animal(db: Session, animal: Animal):
    id_list = db.query(AnimalSpecies.id).all() 
    id_list = [item[0] for item in id_list]
    print(f"{animal.animal_id=}")
    if animal.animal_id in id_list:
        db_animal = AnimalRecord(
            name=animal.name,
            description=animal.description,
            weight=animal.weight,
            arrival_date=animal.arrival_date,
            animal_id=animal.animal_id
        )
        db.add(db_animal)
        db.commit()
        db.refresh(db_animal)
        return db_animal
    else:
        return None
    
def create_user(db: Session, user: User_schema):
    print("creation lololol")
    record = db.query(User).filter(User.username == user.username).first()
    print(record)
    print('record here')
    if record:
        raise HTTPException(status_code=409, detail="Username already taken")
    
    print("hashing")
    print(user.password)
    print(user.password.encode())
    hash_pass = hashlib.sha256(user.password.encode()).hexdigest()
    
    print(hash_pass)
    
    new_user = User(username=user.username,
                    password=hash_pass,
                    created_at = datetime.now(),
                    updated_at = datetime.now(),
                    category_id=2) #category_id=2 : User type
    print(f"{new_user=}")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"{new_user=}")
    return new_user