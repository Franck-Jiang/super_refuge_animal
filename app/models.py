from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, UUID, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from db import Base
from datetime import datetime
class AnimalSpecies(Base):
    __tablename__ = 'animal_species'

    id = Column(Integer, primary_key=True, autoincrement=True)
    species_name = Column(String(100), nullable=False, unique=True)
    food = Column(String(100))

    def __repr__(self):
        return f"<AnimalSpecies(id={self.id}, specie_name='{self.species_name}', food='{self.food}')>"

class AnimalRecord(Base):
    __tablename__ = 'animal_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    weight = Column(Float)
    arrival_date = Column(Date)
    animal_id = Column(Integer, ForeignKey('animal_species.id'), nullable=False)
    animal = relationship("AnimalSpecies", backref="animal_records")
    adopted = Column(Boolean)
    
    def __repr__(self):
        return f"<AnimalRecord(id={self.id}, name='{self.name}', animal_id={self.animal_id}, weight={self.weight}, arrival_date='{self.arrival_date}')>"

class UserCategory(Base):
    __tablename__ = "user_category"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String)

    # Relation vers User
    users = relationship("User", back_populates="user_category")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    category_id = Column(Integer, ForeignKey('user_category.id'), nullable=False)

    user_category = relationship("UserCategory", back_populates="users")
    
    def __repr__(self):
        return (
            f"<User(id={self.id}, username='{self.username}', category_id={self.category_id}, "
            f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"
        )    
class Adoption(Base):
    __tablename__ = "adoption_list"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey('animal_records.id'), nullable=False)
    user_adopter_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    validated = Column(Boolean)
    worker_validation_id = Column(Integer, ForeignKey('user.id'))
    adoption_date = Column(DateTime)
    
    def __repr__(self):
        return (
            f"<Adoption(id={self.id}, animal_id={self.animal_id}, user_adopter_id={self.user_adopter_id}, "
            f"validated={self.validated}, worker_validation_id={self.worker_validation_id}, "
            f"adoption_date='{self.adoption_date}')>"
        )