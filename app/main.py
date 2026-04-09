from fastapi import FastAPI
from database import get_db, Base, engine
from routers import r_auth, r_chat
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(r_auth.router)
app.include_router(r_chat.router)