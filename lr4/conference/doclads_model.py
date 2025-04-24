from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class DocladCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1)
    created_at: datetime
    room_id: Optional[int] = None

class DocladResponse(BaseModel):
    id: str
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1)
    created_at: datetime
    room_id: Optional[int] = None
    