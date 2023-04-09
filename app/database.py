from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . config import settings


"""Create the database connection URL using the values from the settings"""
SQLALCHEMY_DATABASE_URL  = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

"""Create an SQLAlchemy engine instance that will allow us to interact with the database"""
engine = create_engine(SQLALCHEMY_DATABASE_URL)

"""Create a SessionLocal class which we will use to create database sessions"""
SessionLocal = sessionmaker(autocommit = False,autoflush=False , bind=engine)

"""Create a declarative base class that will be the base class for our database models"""
Base = declarative_base()

def get_db():

    """
    Function to get a new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
 