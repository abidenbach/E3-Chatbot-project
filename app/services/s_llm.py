import httpx
import json
from datetime import datetime
from sqlalchemy.orm import Session
import uuid
from models import Contact, Prompt, Chat, Message, Billet, Concert, Artiste, Salle, StyleMusical
from dotenv import load_dotenv
from services.s_auth import decode_token
import os

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"


def _build_and_send(
    q: str,
    id_context: int,
    id_chat: str | None,
    id_utilisateur: int,
    data: list[dict],
    data_label: str,
    db: Session
) -> dict:
    prompt = db.query(Prompt).filter(Prompt.id_prompt == id_context).first()
    if not prompt:
        raise ValueError(f"Prompt {id_context} introuvable")

    full_prompt = (
        f"{prompt.contexte}\n\n"
        f"{data_label} :\n{json.dumps(data, ensure_ascii=False, default=str)}\n\n"
        f"Question : {q}"
    )

    if not id_chat:
        id_chat = str(uuid.uuid4())
        db.add(Chat(
            uuid_chat=id_chat,
            created_at=datetime.utcnow(),
            id_utilisateur=id_utilisateur,
            id_prompt=id_context
        ))
        db.flush()

    db.add(Message(
        uuid_message=str(uuid.uuid4()),
        role="user",
        contenu=q,
        date_creation=datetime.utcnow(),
        uuid_chat=id_chat
    ))

    response = httpx.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": full_prompt, "stream": False},
        timeout=60.0
    )
    response.raise_for_status()
    reponse = response.json()["response"]

    db.add(Message(
        uuid_message=str(uuid.uuid4()),
        role="assistant",
        contenu=reponse,
        date_creation=datetime.utcnow(),
        uuid_chat=id_chat
    ))
    db.commit()

    return {"id_chat": id_chat, "reponse": reponse}


def query_contact(q: str, id_context: int, id_chat: str | None, db: Session, token: str) -> dict:
    id_utilisateur = int(decode_token(token)["sub"])
    data = [
        {"tel": c.tel, "adresse": c.adresse, "mail": c.mail}
        for c in db.query(Contact).all()
    ]
    print(data)
    return _build_and_send(q, id_context, id_chat, id_utilisateur, data, "Données de contact", db)


def query_tickets(q: str, id_context: int, id_chat: str | None, db: Session, token: str) -> dict:
    id_utilisateur = int(decode_token(token)["sub"])
    concerts = (
        db.query(Concert, Artiste, Salle, StyleMusical)
        .join(Artiste, Concert.id_artiste == Artiste.id_artiste)
        .join(Salle, Concert.id_salle == Salle.id_salle)
        .join(StyleMusical, Artiste.id_style == StyleMusical.id_style)
        .all()
    )
    data = [
        {
            "label": c.label,
            "description": c.description,
            "date_debut": c.date_debut,
            "date_fin": c.date_fin,
            "artiste": a.nom_scene,
            "style": sm.label,
            "salle": s.label
        }
        for c, a, s, sm in concerts
    ]
    return _build_and_send(q, id_context, id_chat, id_utilisateur, data, "Concerts disponibles", db)



def query_my_ticket(q: str, id_context: int, id_chat: str | None, db: Session, token: str) -> dict:
    id_utilisateur = int(decode_token(token)["sub"])
    billets = (
        db.query(Billet, Concert, Artiste)
        .join(Concert, Billet.id_concert == Concert.id_concert)
        .join(Artiste, Concert.id_artiste == Artiste.id_artiste)
        .filter(Billet.id_utilisateur == id_utilisateur)
        .all()
    )
    data = [
        {
            "id_billet": b.id_billet,
            "date_achat": b.date_achat,
            "date_valide": b.date_valide,
            "concert": c.label,
            "date_debut": c.date_debut,
            "date_fin": c.date_fin,
            "artiste": a.nom_scene
        }
        for b, c, a in billets
    ]
    return _build_and_send(q, id_context, id_chat, id_utilisateur, data, "Billets de l'utilisateur", db)


def query_salle(q: str, id_context: int, id_chat: str | None, db: Session, token: str) -> dict:
    id_utilisateur = int(decode_token(token)["sub"])
    data = [
        {"label": s.label, "chemin": s.chemin}
        for s in db.query(Salle).all()
    ]
    return _build_and_send(q, id_context, id_chat, id_utilisateur, data, "Informations salles", db)


def query_show(q: str, id_context: int, id_chat: str | None, db: Session, token: str) -> dict:
    id_utilisateur = int(decode_token(token)["sub"])
    concerts = (
        db.query(Concert, Artiste, Salle)
        .join(Artiste, Concert.id_artiste == Artiste.id_artiste)
        .join(Salle, Concert.id_salle == Salle.id_salle)
        .all()
    )
    data = [
        {
            "label": c.label,
            "description": c.description,
            "date_debut": c.date_debut,
            "date_fin": c.date_fin,
            "artiste": a.nom_scene,
            "salle": s.label
        }
        for c, a, s in concerts
    ]
    return _build_and_send(q, id_context, id_chat, id_utilisateur, data, "Spectacles", db)

def query_menu():
    pass