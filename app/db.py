import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

username = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{username}:{password}@db:5432/{db_name}"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()