from typing import Iterable
from sqlalchemy.orm import Session
from app.models import sql_models as m

def add(db: Session, recommendation: m.Recommendation) -> m.Recommendation:
    """Adaugă o nouă recomandare de carte în baza de date."""
    db.add(recommendation)
    db.flush()
    db.refresh(recommendation)
    return recommendation

def list_for_conversation(db: Session, conversation_id: str) -> Iterable[m.Recommendation]:
    """Obține toate recomandările dintr-o conversație, cele mai noi primele."""
    return (
        db.query(m.Recommendation)
        .filter(m.Recommendation.conversation_id == str(conversation_id))
        .order_by(m.Recommendation.created_at.desc())
        .all()
    )