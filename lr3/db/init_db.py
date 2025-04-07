
from sqlalchemy.orm import Session
from db.database import engine, Base
from db.test_data import USERS_DATA, ROOMS_DATA, DOCLADS_DATA
from passlib.context import CryptContext
from db.database import User, Room, Doclads  


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db(): 
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    try:
        if db.query(User).count() == 0:
            test_users = [
                User(
                    username=user["username"],
                    login=user["login"],
                    password=pwd_context.hash(user["password"]),
                    role=user["role"]
                )
                for user in USERS_DATA
            ] 
            db.add_all(test_users)
            db.flush()
            
            test_rooms = [
                Room(title=room["title"])
                for room in ROOMS_DATA
            ]
            db.add_all(test_rooms)
            db.flush()
    
            test_doclads = [
                Doclads(
                    title=doclad["title"],
                    author=doclad["author"],
                    room_id=doclad.get("room_id")
                )
                for doclad in DOCLADS_DATA
            ]
            
            db.add_all(test_doclads)
            
            db.commit()
      
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()