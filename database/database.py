import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine, text
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
def connect():
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}"
    return create_engine(DATABASE_URL)

def fetchAllUsers():
    engine = connect()
    with engine.connect() as connection:
        result = connection.execute(text("SELECT user_id, profession,likings, current_project FROM users"))
        profiles = [dict(row) for row in result.mappings()]
    
    return profiles