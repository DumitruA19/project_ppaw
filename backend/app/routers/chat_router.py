from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import get_current_user
from app.models import schema as s
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Smart Librarian Chat"])

@router.post("/", response_model=s.ChatResponse)
def ask_librarian(
    request: s.ChatRequest, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """
    Endpoint principal: Trimite un mesaj bibliotecarului inteligent.
    Include validare de securitate (JWT) și verificare de abonament.
    """
    try:
        service = ChatService(db)
        return service.process_chat(current_user, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare internă de sistem: {str(e)}")