from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, UUID, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from db import Base
from datetime import datetime

class Owner(Base):
    __tablename__ = 'owner'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(15))
    created_at = Column(Date)

    def __repr__(self):
        return f"<Owner(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', phone='{self.phone}')>"

class AnimalList(Base):
    __tablename__ = 'animal_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    specie_name = Column(String(100), nullable=False, unique=True)
    food = Column(String(100))

    def __repr__(self):
        return f"<AnimalList(id={self.id}, specie_name='{self.specie_name}', food='{self.food}')>"

class AnimalRecord(Base):
    __tablename__ = 'animal_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    weight = Column(Float)
    arrival_date = Column(Date)
    animal_id = Column(Integer, ForeignKey('animal_list.id'), nullable=False)
    animal = relationship("AnimalList", backref="animal_records")

    def __repr__(self):
        return f"<AnimalRecord(id={self.id}, name='{self.name}', species_id={self.species_id}, weight={self.weight}, arrival_date='{self.arrival_date}')>"

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
    
