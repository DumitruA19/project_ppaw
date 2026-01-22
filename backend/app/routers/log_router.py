from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.log_services import LogService #
from app.core.security import require_admin # Recomandat pentru securitate

router = APIRouter(prefix="/logs", tags=["System Logs"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_log(data: dict, db: Session = Depends(get_db)):
    """
    Endpoint pentru înregistrarea log-urilor.
    Așteaptă: action, user_id (optional), metadata (dict optional), meta (optional).
    """
    return LogService(db).log_event(
        action=data.get("action", "UNKNOWN_ACTION"),
        user_id=data.get("user_id"),
        metadata=data.get("metadata"),
        meta=data.get("meta")
    )