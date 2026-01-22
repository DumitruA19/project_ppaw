from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import get_current_user #
from app.services.account_service import AccountService
from app.models import schema as s #

router = APIRouter(prefix="/account", tags=["User Account"])

@router.get("/me", response_model=s.UserOut)
def get_my_profile(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Punct de acces pentru datele de profil."""
    return AccountService(db).get_profile(user)

@router.post("/change-password")
def update_password(
    data: s.PasswordChange, # Folosim schema specifică
    user=Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Ruta pentru securitatea contului."""
    try:
        # Pasați argumentele direct din schema validată
        return AccountService(db).change_password(user, data.old_password, data.new_password)
    except ValueError as e:
        # Transformăm eroarea de logică în eroare HTTP 400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/overview")
def get_account_overview(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Dashboard rapid pentru utilizator (Abonament + Consum)."""
    return AccountService(db).get_overview(user)