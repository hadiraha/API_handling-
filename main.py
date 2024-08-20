#FastAPI Applications
from dotenv import load_dotenv
import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import crud, database, models, schemas
from typing import List
import uvicorn
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

load_dotenv()
SECRET_KEY = os.getenv('secret_key')
ALGORITHM = os.getenv('algorithm')
ACCESS_TOKEN_EXPIRE_MINUTES = 120

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/home", StaticFiles(directory= r"static\home"), name="static")
app.mount("/static/login", StaticFiles(directory= r"static\login"), name="static")
app.mount("/static/register", StaticFiles(directory= r"static\register"), name="static")

database.init_db()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception   = HTTPException(
        status_code=401,
        detail= "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db=db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token/", response_model=dict)
def login_for_access_token(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authentication_user(db, from_data.username, from_data.password)
    if not user:
        raise HTTPException(status_code=401,detail="Incorrect user or pass or both or...!!!")
    access_token = create_access_token(data = {"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
    
@app.get("/")
def read_root():
    return {"message": "Go to /static/home/index.html to view the home page."}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, username=user.username, password=user.password)

@app.get("/profiles/{id}", response_model=schemas.Profile)
def read_profile(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    logger.info(f"Fetching profile with id: {id}")
    db_profile = crud.get_profile(db, id=id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return schemas.Profile.model_validate(db_profile)

@app.get("/profiles/", response_model=List[schemas.Profile])
def read_profiles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    logger.info(f"Fetching profiles with skip: {skip}, limit: {limit}")
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return [schemas.Profile.model_validate(profile) for profile in profiles]

@app.get("/usernames/", response_model=List[str])
def read_usernames(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    logger.info(f"Fetching profiles with skip: {skip}, limit: {limit}")
    usernames = crud.get_usernames(db, skip=skip, limit=limit)
    return [username[0] for username in usernames]

@app.get("/profiles/username/{username}", response_model=schemas.Profile)
def read_profile_by_username(username: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    logger.info(f"Fetching profile with username: {username}")
    db_profile = crud.get_profile_by_username(db, username=username)
    return schemas.Profile.model_validate(db_profile)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)