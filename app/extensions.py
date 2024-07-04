import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))
try:
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Успешное подключение к БД")
except Exception as e:
    print("Ошибка подключения к БД", e)
Session = sessionmaker(bind=engine)

Base = declarative_base()