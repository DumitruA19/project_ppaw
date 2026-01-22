from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import get_current_user
from app.models import schema as s
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["Chat Conversations"])

@router.get("/", response_model=list[s.ConversationOut])
def list_my_chats(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return ConversationService(db).get_user_conversations(current_user.id)

@router.post("/", response_model=s.ConversationOut)
def start_new_chat(data: s.ConversationCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return ConversationService(db).create_conversation(current_user.id, data.title)