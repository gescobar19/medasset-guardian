import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://summitsafe:summitsafe_pw@localhost:5432/summitsafe"
)
print("DATABASE_URL =", DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # helps prevent stale connections
)
print("ENGINE =", engine.url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()