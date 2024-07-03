import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"), echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()