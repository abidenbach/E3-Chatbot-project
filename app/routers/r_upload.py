# routers/contact.py
from fastapi import APIRouter, Form, Depends, HTTPException
from database import get_db

router = APIRouter(prefix="/administration", tags=["Administration"])

@router.post("/upload")   # POST /administration/upload
def upload():
    pass