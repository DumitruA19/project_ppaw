from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.core.db import get_db
from app.core.security import get_current_user
from app.services.usage_service import UsageService

router = APIRouter(prefix="/usage", tags=["Resource Usage"])

@router.get("/")
def read_usage(
    start: date, 
    end: date, 
    current_user=Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Punct de acces pentru vizualizarea consumului curent."""
    service = UsageService(db)
    usage = service.get_user_usage(current_user.id, start, end)
    if not usage:
        raise HTTPException(status_code=404, detail="Nu s-au găsit date de consum pentru această perioadă.")
    return usage