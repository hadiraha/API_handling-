#DataBase connectins
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv('host')
DB_USER = os.getenv('user')
DB_PASS = os.getenv('pass')
DB_NAME = os.getenv('database')
DB_AUTH = os.getenv('auth_plugin')

##Define database url address ##Note that do not put space in ""
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
