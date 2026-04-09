from fastapi import APIRouter, Form, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.s_auth import authenticate_user, create_access_token, information_user

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/login")   # POST /auth/login
def login(mail: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, mail, password)
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token({"sub": str(user.id_utilisateur)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")       # GET /auth/me
def me(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.removeprefix("Bearer ")
    user = information_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    return {
        "id": user.id_utilisateur,
        "nom": user.nom,
        "prenom": user.prenom,
        "mail": user.mail
}