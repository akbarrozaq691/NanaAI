from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os

load_dotenv()

def read_db():
    # Database credentials
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    
    # PostgreSQL connection string format
    connection_string = f"postgresql://{username}:{password}@{host}/{database}?sslmode=require"
    engine = create_engine(connection_string)

    # # Initialize SQLDatabase object with required tables
    db = SQLDatabase(
        engine,
        view_support=True
    )
    return db