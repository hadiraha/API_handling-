#FastAPI Applications
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import crud, database, models, schemas
from typing import List
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

database.init_db()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/profiles/{id}", response_model=schemas.Profile)
def read_profile(id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching profile with id: {id}")
    db_profile = crud.get_profile(db, id=id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return schemas.Profile.model_validate(db_profile)

@app.get("/profiles/", response_model=List[schemas.Profile])
def read_profiles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching profiles with skip: {skip}, limit: {limit}")
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return [schemas.Profile.model_validate(profile) for profile in profiles]

@app.get("/usernames/", response_model=List[str])
def read_usernames(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    logger.info(f"Fetching profiles with skip: {skip}, limit: {limit}")
    usernames = crud.get_usernames(db, skip=skip, limit=limit)
    return [username[0] for username in usernames]

@app.get("/profiles/username/{username}", response_model=schemas.Profile)
def read_profile_by_username(username: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching profile with username: {username}")
    db_profile = crud.get_profile_by_username(db, username=username)
    return schemas.Profile.model_validate(db_profile)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)