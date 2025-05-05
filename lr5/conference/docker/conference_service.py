from fastapi import HTTPException, FastAPI, Depends
from conference.doclads_model import DocladCreate, DocladResponse
from typing import List
from .room_model import RoomCreate, RoomResponse
from sqlalchemy.orm import Session
from db.database import Room, User
from sqlalchemy.orm import Session
from db.session_mongodb import collection
from db.session_postgresql import get_db
from auth.auth import get_current_client
from datetime import datetime  
from bson import ObjectId

from auth.auth import router as auth_touter

app = FastAPI()
app.include_router(auth_touter, prefix="/auth", tags=["auth"])

def doclad_helper(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "title": doc.get("title", ""),
        "author": doc.get("author", ""),
        "content": doc.get("content", ""),
        "room_id": doc.get("room_id"),
        "created_at": doc.get("created_at")
    }

@app.post("/doclads/", response_model=DocladResponse)
def create_doclad(doclad: DocladCreate, current_user: User = Depends(get_current_client)):
    data = doclad.dict()
    data["created_at"] = datetime.utcnow()
    result = collection.insert_one(data)
    new_doclad = collection.find_one({"_id": result.inserted_id})
    return doclad_helper(new_doclad)


@app.get("/doclads_all/", response_model=list[DocladResponse])
def get_all_doclads():
    return [doclad_helper(doc) for doc in collection.find()]

@app.get('/search/{doclad_title}', response_model=List[DocladResponse])
async def get_title(doclad_title: str):
    query = {"title": {"$regex": doclad_title, "$options": "i"}}  
    doclads = collection.find(query)
    result = [doclad_helper(doc) for doc in doclads]
    if not result:
        raise HTTPException(status_code=404, detail="Doclad not found")
    return result

@app.put("/{doclad_id}", response_model=DocladResponse)
async def update_doclad(doclad_id: str, update: DocladCreate,  current_user: User = Depends(get_current_client)):
    query = {"_id": ObjectId(doclad_id)} 
    existing_doclad = collection.find_one(query)
    if not existing_doclad:
        raise HTTPException(status_code=404, detail="Doclad not found")
    update_data = update.dict(exclude_unset=True)
    result = collection.update_one(query, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Doclad not found")
    updated_doclad = collection.find_one(query)
    return doclad_helper(updated_doclad)

    
@app.delete("/{doclad_id}", response_model=DocladResponse)
async def delete_doclad(doclad_id: str,  current_user: User = Depends(get_current_client)):
    doclad = collection.find_one({"_id": ObjectId(doclad_id)})
    if not doclad:
        raise HTTPException(status_code=404, detail="Doclad not found")
    collection.delete_one({"_id": ObjectId(doclad_id)})
    return DocladResponse(
        id=doclad["_id"], 
        title=doclad["title"],
        author=doclad["author"],
        content=doclad["content"],
        created_at=doclad["created_at"]
    )

@app.post("/rooms/", response_model=RoomResponse)
async def create_room(rooms: RoomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    room = Room(**rooms.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@app.get("/rooms_all/", response_model=List[RoomResponse])
async def get_all_rooms(db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    rooms = db.query(Room).order_by(Room.id).all()
    return rooms

@app.put("/doclads/{doclad_id}/add_to_room/{room_id}", response_model=DocladResponse)
async def add_doclad_to_room(doclad_id: str, room_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    doclad = collection.find_one({"_id": ObjectId(doclad_id)})
    if not doclad:
        raise HTTPException(status_code=404, detail="Doclad not found")
    collection.update_one(
        {"_id": ObjectId(doclad_id)},
        {"$set": {"room_id": room_id, "updated_at": datetime.utcnow()}}
    )
    updated = collection.find_one({"_id": ObjectId(doclad_id)})
    return doclad_helper(updated)

@app.get("/{room_id}/doclads", response_model=List[DocladResponse])
async def get_conference_doclads(room_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    doclads = list(collection.find({"room_id": room_id}))
    for doclad in doclads:
        doclad["id"] = str(doclad["_id"])
    return doclads