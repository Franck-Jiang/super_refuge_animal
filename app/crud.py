from sqlalchemy.orm import Session
from schemas.animal import Species, Animal
from models import AnimalSpecies, AnimalRecord

 
def create_species(db: Session, specie: Species) -> AnimalSpecies:
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