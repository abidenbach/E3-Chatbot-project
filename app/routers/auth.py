# routers/auth.py
from fastapi import APIRouter, Form, Depends, HTTPException
from database import get_db

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/login")   # POST /auth/login
def login(mail: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, mail, password)
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")       # GET /auth/me
def me():
    pass 