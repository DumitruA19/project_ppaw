# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.core.db import get_db
# from app.core.security import get_current_user # Adăugat pentru securitate
# from app.models import schema as s
# from app.services.message_service import MessageService

# router = APIRouter(prefix="/messages", tags=["Chat History"])

# @router.get("/{conversation_id}", response_model=list[s.MessageOut])
# def get_messages_by_conversation(
#     conversation_id: str, 
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user) # Verifică dacă userul este logat
# ):
#     """Returnează toate mesajele dintr-o conversație specifică."""
#     service = MessageService(db)
#     # Notă: Aici se poate adăuga o verificare extra dacă conv_id aparține de current_user.id
#     return service.list_messages(conversation_id)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import schema as s
# Nota: Va trebui sa creezi si MessageService ulterior
# from app.services.message_service import MessageService 

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.get("/{conversation_id}", response_model=list[s.MessageOut])
def get_messages(conversation_id: str, db: Session = Depends(get_db)):
    # Simulare returnare mesaje pana la crearea serviciului
    return []