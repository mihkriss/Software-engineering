from fastapi import FastAPI
from conference.conference_service import router as conference_router
from user.auth import router as auth_touter
from user.user_service import router as user_router
from db.init_db import init_db
from db.database import create_tables


app = FastAPI()

create_tables()
init_db()

app.include_router(auth_touter, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(conference_router, prefix="/conference", tags=["conference"])

@app.get("/")
async def read_root():
    return {"message": "Welcome Conferences website"}



