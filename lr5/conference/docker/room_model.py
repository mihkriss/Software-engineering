from pydantic import BaseModel

class RoomCreate(BaseModel):
    title: str

class RoomResponse(BaseModel):
    title: str
    id: int
    
    class Config:
        from_attributes = True


