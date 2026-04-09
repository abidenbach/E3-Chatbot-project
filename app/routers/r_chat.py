from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid
from database import get_db
from models import Chat, Message
from services.s_llm import query_contact, query_tickets, query_my_ticket, query_salle, query_show

router = APIRouter(prefix="/chat", tags=["Chat"])

DISPATCH = {
    1: query_tickets,
    2: query_my_ticket,
    3: query_salle,
    4: query_show,
    5: query_contact,
}

class ChatRequest(BaseModel):
    id_chat: Optional[str] = None
    q: str


@router.post("/{id_contexte}")
def send_message(
    id_contexte: int,
    body: ChatRequest,
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    token = authorization.removeprefix("Bearer ")

    handler = DISPATCH.get(id_contexte)
    if not handler:
        raise HTTPException(status_code=404, detail=f"Contexte {id_contexte} inconnu")

    try:
        result = handler(
            q=body.q,
            id_context=id_contexte,
            id_chat=body.id_chat,
            db=db,
            token=token
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result


@router.get("/{id_chat}")
def get_chat(
    id_chat: uuid.UUID,
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    chat = db.query(Chat).filter(Chat.uuid_chat == str(id_chat)).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat introuvable")

    messages = (
        db.query(Message)
        .filter(Message.uuid_chat == str(id_chat))
        .order_by(Message.date_creation)
        .all()
    )

    return {
        "id_chat": str(id_chat),
        "messages": [
            {"role": m.role, "contenu": m.contenu, "timestamp": m.date_creation}
            for m in messages
        ]
    }
