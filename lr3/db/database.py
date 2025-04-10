
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, ForeignKey, create_engine, Column, Integer, Index
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

    __table_args__ = (
        Index('ix_users_username', 'username', postgresql_using='gin', postgresql_ops={"username": "gin_trgm_ops"}),
        Index('ix_users_login', 'login', postgresql_using='gin', postgresql_ops={"login": "gin_trgm_ops"}),
    )

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    doclads = relationship("Doclads", back_populates="room")

    __table_args__ = (
        Index('ix_rooms_title', 'title', postgresql_using='gin', postgresql_ops={"title": "gin_trgm_ops"}),
    )

class Doclads(Base):
    __tablename__ = "doclads"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)

    room = relationship("Room", back_populates="doclads")

    __table_args__ = (
        Index('ix_doclads_title', 'title', postgresql_using='gin', postgresql_ops={"title": "gin_trgm_ops"}),
    )

