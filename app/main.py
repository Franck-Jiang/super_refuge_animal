from fastapi import FastAPI
from app import api


app = FastAPI(
    title="Super refuge",
    description="Un super projet de super site web",
    version="0.0.1",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI project!"}

# Include other routes from `api.py`
app.include_router(api.router)
