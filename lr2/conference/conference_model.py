from pydantic import BaseModel
from typing import List, Optional

class Doclad(BaseModel):
    title: str
    author: str

class Room(BaseModel):
    title: str
    doclads: List[Doclad] = []