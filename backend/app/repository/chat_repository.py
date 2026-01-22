from sqlalchemy.orm import Session
from app.models import sql_models as m

# === Gestiune Conversații ===
def create_conversation(db: Session, user_id: str, title: str = None) -> m.Conversation:
    """Creează o nouă conversație în MySQL folosind UUID ca string."""
    conv = m.Conversation(user_id=user_id, title=title)
    db.add(conv)
    db.flush()
    db.refresh(conv)
    return conv

def get_conversation(db: Session, conv_id: str):
    """Căutare după ID-ul de tip string."""
    return db.query(m.Conversation).filter(m.Conversation.id == conv_id).first()

def list_conversations_for_user(db: Session, user_id: str):
    """Returnează istoricul conversațiilor ordonat descrescător."""
    return (
        db.query(m.Conversation)
        .filter(m.Conversation.user_id == user_id)
        .order_by(m.Conversation.created_at.desc())
        .all()
    )

# === Gestiune Mesaje ===
def add_message(db: Session, conversation_id: str, role: str, content: str) -> m.Message:
    """Adaugă un mesaj nou (user sau assistant)."""
    msg = m.Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    db.flush()
    db.refresh(msg)
    return msg

def get_history(db: Session, conversation_id: str, limit: int = 10):
    """Recuperează ultimele mesaje pentru a oferi context modelului AI."""
    return (
        db.query(m.Message)
        .filter(m.Message.conversation_id == conversation_id)
        .order_by(m.Message.created_at.desc())
        .limit(limit)
        .all()
    )[::-1] # Inversăm pentru a avea ordinea cronologică corectă