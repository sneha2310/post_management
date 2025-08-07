# raw db connection using psycopg2
# import psycopg2
# from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import  settings

engine = create_engine(f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}", echo=True)  # echo=True for debugging SQL queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# raw db connection using psycopg2
# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='test', password='password', port='5433', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connection established successfully.")
# except psycopg2.OperationalError as e:
#     print("Database connection failed. Please check your database settings.")
#     print(f"Error: {e}")
