from fastapi import HTTPException, FastAPI, Depends
from .users_model import UserCreate, UserResponse, UserUpdate
from sqlalchemy.orm import Session
from db.database import User
from typing import List
from db.session_postgresql import get_db
from passlib.context import CryptContext
from auth.auth import get_current_client
from auth.auth import router as auth_touter
from db.init_db import init_db
from db.database import create_tables

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
    return user

@app.get("/{users_all}/", response_model=List[UserResponse])
async def get_user_all(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id).all()
    return users

@app.get("/{user_login}", response_model=UserResponse)
async def get_user_login(user_login: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == user_login).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
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
    hashed_password = pwd_context.hash(update_data["password"])

    if "password" in update_data:
        update_data["password"] = hashed_password

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
    

@app.delete("/{user_id}", response_model=UserResponse, )
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user