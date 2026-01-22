from typing import Iterable, Optional
from sqlalchemy.orm import Session
from app.models import sql_models as m

def list_users(db: Session) -> Iterable[m.User]:
    """Obține toți utilizatorii ordonați după data înregistrării."""
    return db.query(m.User).order_by(m.User.created_at.desc()).all()

def get_by_id(db: Session, user_id: str) -> Optional[m.User]:
    """Căutare după ID (string/UUID) în MySQL."""
    return db.query(m.User).filter(m.User.id == str(user_id)).first()

def get_by_email(db: Session, email: str) -> Optional[m.User]:
    """Căutare după email pentru validări."""
    return db.query(m.User).filter(m.User.email == email).first()

def add(db: Session, user: m.User) -> m.User:
    """Adaugă un obiect User în baza de date."""
    db.add(user)
    db.flush()
    db.refresh(user)
    return user

def delete(db: Session, user: m.User) -> None:
    """Șterge definitiv un utilizator."""
    db.delete(user)
    db.flush()