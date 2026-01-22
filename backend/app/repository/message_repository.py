from typing import Iterable
from sqlalchemy.orm import Session
from app.models import sql_models as m

def add(db: Session, message: m.Message) -> m.Message:
    """Salvează un mesaj nou (utilizator sau AI) în baza de date."""
    db.add(message)
    db.flush()
    db.refresh(message)
    return message

def list_for_conversation(db: Session, conversation_id: str) -> Iterable[m.Message]:
    """Recuperează toate mesajele dintr-o sesiune, ordonate de la cel mai vechi la cel mai nou."""
    return (
        db.query(m.Message)
        .filter(m.Message.conversation_id == str(conversation_id))
        .order_by(m.Message.created_at.asc())
        .all()
    )