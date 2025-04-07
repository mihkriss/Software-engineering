from fastapi import HTTPException, APIRouter, Depends
from conference.conference_model import DocladCreate, DocladResponse, RoomCreate, RoomResponse
from typing import List
from sqlalchemy.orm import Session
from db.database import Doclads, Room
from sqlalchemy.orm import Session
from db.sessions import get_db
from user.auth import get_current_client
from db.database import User


router = APIRouter()

@router.post("/doclads/", response_model=DocladResponse)
async def create_doclad(doclad: DocladCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    doclad =Doclads(title=doclad.title, author=doclad.author)

    db.add(doclad)
    db.commit()
    db.refresh(doclad)
    return doclad


@router.get("/doclads_all/", response_model=List[DocladResponse])
async def get_doclad_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    doclads = db.query(Doclads).order_by(Doclads.id).all()
    return doclads

@router.get('/search/{doclad_title}', response_model=List[DocladResponse])
async def get_title(title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    doclads = db.query(Doclads).order_by(Doclads.id).filter(Doclads.title.ilike(f"%{title}%")).all()
    if not doclads:
        raise HTTPException(status_code=404, detail="Doclad not found")
    return doclads

@router.put("/{doclad_id}", response_model=DocladResponse)
async def update_doclad(doclad_id: int, update: DocladCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    doclad = db.get(Doclads, doclad_id)
    if not doclad:
        raise HTTPException(status_code=404, detail="Doclad not found")

    update_data = update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(doclad, field, value)

    db.commit()
    db.refresh(doclad)
    return doclad
    
@router.delete("/{doclad_id}", response_model=DocladResponse)
async def delete_doclad(doclad_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    doclad = db.get(DocladResponse, doclad_id)
    if not doclad:
        raise HTTPException(status_code=404, detail="Doclad not found")
    db.delete(doclad)
    db.commit()
    return doclad

@router.post("/rooms/", response_model=RoomResponse)
async def create_room(rooms: RoomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    room = Room(**rooms.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.get("/rooms_all/", response_model=List[RoomResponse])
async def get_all_rooms(db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    rooms = db.query(Room).order_by(Room.id).all()
    return rooms

@router.put("/doclads/{doclad_id}/add_to_room/{room_id}", response_model=DocladResponse)
async def add_doclad_to_room(doclad_id: int, room_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    doclad = db.get(Doclads, doclad_id)
    if not doclad:
        raise HTTPException(status_code=404, detail="Doclad not found")
    
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    doclad.room_id = room_id
    db.commit()
    db.refresh(doclad)
    return doclad

@router.get("/{room_id}/doclads", response_model=List[DocladResponse])
async def get_conference_doclads(room_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    room= db.get(Room, room_id)
    if not room: 
        raise HTTPException(status_code=404, detail="Room not found")
    return room.doclads
