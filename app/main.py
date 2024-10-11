from fastapi import FastAPI
from sqlalchemy import select
from models import AnimalRecord
from db import session


app = FastAPI(
    title="Super refuge",
    description="Un super projet de super site web",
    version="0.0.1",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI project!"}

@app.get("/animals")
def get_animals():
    stmt = select(AnimalRecord)
    res = session.execute(stmt)
    return res
# Include other routes from `api.py`
#app.include_router(api.router)
