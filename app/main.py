from fastapi import FastAPI
from database import get_db, Base, engine
from routers import r_auth
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(r_auth.router)
