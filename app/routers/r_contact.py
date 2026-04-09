# routers/contact.py
from fastapi import APIRouter, Form, Depends, HTTPException
from database import get_db

router = APIRouter(prefix="/informations", tags=["Informations"])

@router.get("/contacts")   # GET /informations/contacts
def contacts():
    pass