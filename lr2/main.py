from fastapi import FastAPI
from user.auth import router as auth_router
from user.user_service import router as user_router
from conference.conference_service import router as conference_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(conference_router, prefix="/conference", tags=["conference"])

@app.get("/")
async def read_root():
    return {"message": "Welcome Conferences website"}
