import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

username = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{username}:{password}@db:5432/{db_name}"
engine = create_engine(DATABASE_URL)

Base = declarative_base()
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()

def get_db():
    try:
        db = session
        yield db
    finally:
        db.close()