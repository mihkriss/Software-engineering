
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, ForeignKey, create_engine, Column, Integer
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/conference")
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    doclads = relationship("Doclads", back_populates="room")

class Doclads(Base):
    __tablename__ = "doclads"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)

    room = relationship("Room", back_populates="doclads")

