from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import get_current_user, require_admin
from app.models import schema as s
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("/", response_model=list[s.UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    admin: m.User = Depends(require_admin) # Protejat: doar adminul poate vedea lista
):
    """Obține lista tuturor utilizatorilor (Acces restricționat Admin)."""
    return UserService(db).list_users()

@router.get("/me", response_model=s.UserOut)
def get_my_info(current_user: m.User = Depends(get_current_user)):
    """Returnează informațiile despre utilizatorul logat curent."""
    return current_user

@router.post("/", response_model=s.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: s.UserCreate, db: Session = Depends(get_db)):
    """Endpoint pentru crearea unui cont nou."""
    try:
        return UserService(db).create_user(user_data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))