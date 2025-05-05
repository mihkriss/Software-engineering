from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List
from fastapi.encoders import jsonable_encoder

from .users_model import UserCreate, UserResponse, UserUpdate
from db.database import User
from db.session_postgresql import get_db
from auth.auth import get_current_client
from auth.auth import router as auth_touter
from db.init_db import init_db
from db.database import create_tables
from db.redis_cache import get_cache, set_cache, delete_cache
import json

app = FastAPI()
app.include_router(auth_touter, prefix="/auth", tags=["auth"])

create_tables()
init_db()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.login == user.login).first():
        raise HTTPException(status_code=400, detail="Login already registered")

    hashed_password = pwd_context.hash(user.password)
    user = User(
        username=user.username,
        login=user.login,
        password=hashed_password,
        role=user.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    delete_cache("users_all")
    delete_cache(f"user:{user.login}")

    return user

@app.get("/users/", response_model=List[UserResponse])
async def get_user_all(db: Session = Depends(get_db)):
    cache_key = "users_all"
    cached = get_cache(cache_key)
    if cached:
        return cached  

    users = db.query(User).order_by(User.id).all()
    data = jsonable_encoder(users)
    set_cache(cache_key, data)
    return users

@app.get("/users/{user_login}", response_model=UserResponse)
async def get_user_login(user_login: str, db: Session = Depends(get_db)):
    cache_key = f"user:{user_login}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    user = db.query(User).filter(User.login == user_login).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    data = jsonable_encoder(user)
    set_cache(cache_key, data)
    return user

@app.get('/search/{username}', response_model=List[UserResponse])
async def get_user_name(username: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.username.ilike(f"%{username}%")).all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = update.model_dump(exclude_unset=True)
    if "password" in update_data:
        hashed_password = pwd_context.hash(update_data["password"])
        update_data["password"] = hashed_password

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    delete_cache("users_all")
    delete_cache(f"user:{user.login}")

    return user

@app.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    delete_cache("users_all")
    delete_cache(f"user:{user.login}")

    return user
