from typing import Iterable, Optional
from sqlalchemy.orm import Session
from app.models import sql_models as m

def add(db: Session, conversation: m.Conversation) -> m.Conversation:
    """Persistă o conversație nouă în MySQL."""
    db.add(conversation)
    db.flush()
    db.refresh(conversation)
    return conversation

def get_by_id(db: Session, conversation_id: str) -> Optional[m.Conversation]:
    """Caută o conversație după ID-ul de tip string."""
    return (
        db.query(m.Conversation)
        .filter(m.Conversation.id == str(conversation_id))
        .first()
    )

def list_for_user(db: Session, user_id: str) -> Iterable[m.Conversation]:
    """Returnează lista conversațiilor unui utilizator, cele mai recente primele."""
    return (
        db.query(m.Conversation)
        .filter(m.Conversation.user_id == str(user_id))
        .order_by(m.Conversation.created_at.desc())
        .all()
    )

def remove(db: Session, conversation: m.Conversation) -> None:
    """Șterge o conversație din baza de date."""
    db.delete(conversation)
    db.flush()