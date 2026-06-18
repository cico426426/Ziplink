from sqlalchemy import Column, Integer, String
from database import Base

class Url(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    longURL = Column(String, unique=True, index=True)
    shortURL = Column(String, unique=True, index=True)