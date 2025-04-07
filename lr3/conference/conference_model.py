from pydantic import BaseModel
from typing import Optional

class RoomCreate(BaseModel):
    title: str

class RoomResponse(BaseModel):
    title: str
    id: int
    
    class Config:
        from_attributes = True


class DocladCreate(BaseModel):
    title: str
    author: str
    room_id: Optional[int] = None

class DocladResponse(BaseModel):
    title: str
    author: str
    id: int
    room_id: Optional[int] = None
    
    class Config:
        from_attributes = True

