from fastapi import FastAPI
from database import get_db
from routers import auth

app = FastAPI()

app.include_router(auth.router)
