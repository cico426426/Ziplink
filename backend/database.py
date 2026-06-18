from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() # inherit from this class to create ORM models

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as exc:
        safe_url = engine.url.render_as_string(hide_password=True)
        raise RuntimeError(
            f"Could not connect to the database at {safe_url}. "
            "Start PostgreSQL, create the configured database, or update DATABASE_URL."
        ) from exc

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
