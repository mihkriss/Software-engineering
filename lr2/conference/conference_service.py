from fastapi import HTTPException, APIRouter
from conference.conference_model import Room, Doclad
from typing import List

router = APIRouter()

room_db = []  
doclad_db = [] 

#Создание доклада
@router.post("/doclads/")
async def create_doclad(doclad: Doclad):
    doclad_db.append(doclad)
    return {"message": "Doclad created successfully"}

#Список всех докладов
@router.get("/doclad/", response_model=List[Doclad])
async def get_doclad_all():
    return doclad_db

#Добавление доклада в конференцию
@router.post("/room/{room_title}/doclads")
async def add_doclads_room(room_title: str, doclad: Doclad):
    for room in room_db:
        if room.title == room_title:
           room.doclads.append(doclad)  
           return {"message": f"Doclad added to room '{room_title}' successfully"}
    new_room = Room(title=room_title, doclads=[doclad])
    room_db.append(new_room)
    return {"message": f"Room '{room_title}' created and doclad added successfully"}
  
#Список докладов в конференции
@router.get("/room/{room_title}/doclads")
async def get_doclads_rooms(room_title: str):
    for room in room_db:
        if room.title == room_title:
            return room.doclads
    raise HTTPException(status_code=404, detail="Room not found")