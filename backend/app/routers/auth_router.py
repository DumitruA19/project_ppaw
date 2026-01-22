
# app/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # IMPORTĂ ACESTA
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.auth_service import AuthService
from app.models import schema as s
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=s.UserOut)
def user_register(data: s.UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register(data.email, data.name, data.password, data.role)

@router.post("/login")
# MODIFICARE AICI: data devine OAuth2PasswordRequestForm
def user_login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): 
    """Endpoint standard OAuth2. Așteaptă 'username' (email) și 'password' ca Form Data."""
    return AuthService(db).login(data.username, data.password)

@router.get("/me", response_model=s.UserOut)
def get_current_profile(user=Depends(get_current_user)):
    return user