from fastapi import HTTPException, Query, APIRouter, Depends
from .users_model import UserCreate, UserResponse, UserUpdate
from sqlalchemy.orm import Session
from db.database import User
from typing import List
from db.sessions import get_db
from sqlalchemy import select
from passlib.context import CryptContext
from .auth import get_current_client


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/users/", response_model=UserResponse)
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
    return user

@router.get("/{users_all}/", response_model=List[UserResponse])
async def get_user_all(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id).all()
    return users

@router.get("/{user_login}", response_model=UserResponse)
async def get_user_login(user_login: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == user_login).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get('/search/{username}', response_model=List[UserResponse])
async def get_user_name(username: str, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id).filter(User.username.ilike(f"%{username}%")).all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, update: UserUpdate, db: Session = Depends(get_db),current_user: User = Depends(get_current_client)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = update.model_dump(exclude_unset=True)
    hashed_password = pwd_context.hash(update_data["password"])

    if "password" in update_data:
        update_data["password"] = hashed_password

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
    

@router.delete("/{user_id}", response_model=UserResponse, )
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user