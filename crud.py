#CRUD operations
from sqlalchemy.orm import Session
import models, schemas

##Get one profiles
def get_profile(db: Session, id: int):
    return db.query(models.Profile).filter(models.Profile.id == id).first()

##Get bucket of profiles
def get_profiles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Profile).offset(skip).limit(limit).all()

def get_usernames(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Profile.username).offset(skip).limit(limit).all()

def get_profile_by_username(db: Session, username: str):
    return db.query(models.Profile).filter(models.Profile.username == username).first()