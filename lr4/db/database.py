from sqlalchemy.orm import declarative_base
from sqlalchemy import String, create_engine, Column, Integer, Index, Text, DateTime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/conference")
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

    __table_args__ = (
        Index('ix_rooms_title', 'title', postgresql_using='gin', postgresql_ops={"title": "gin_trgm_ops"}),
    )


