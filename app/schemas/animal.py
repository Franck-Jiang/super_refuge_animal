from pydantic import BaseModel
from datetime import date

class Species(BaseModel):
    specie_name: str
    food: str
    
class Animal(BaseModel):
    name: str
    description: str
    weight: float
    arrival_date: date
    animal_id: int
