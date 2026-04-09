# routers/chat.py
from fastapi import APIRouter, Form, Depends, HTTPException
from database import get_db

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/{id_contexte:int}")   # POST /chat/{id_contexte}
def send_message(id_contexte: int):
    pass

@router.get("/{id_chat:uuid}")       # GET /chat/{id_chat}
def get_chat(id_chat: uuid.UUID):
    pass