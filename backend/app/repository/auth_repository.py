from sqlalchemy.orm import Session
from typing import Optional
from app.models import sql_models as m

def get_by_email(db: Session, email: str) -> Optional[m.User]:
    """Căutare utilizator după email pentru login și validare la register."""
    return db.query(m.User).filter(m.User.email == email).first()

def get_by_id(db: Session, user_id: str) -> Optional[m.User]:
    """Căutare utilizator după ID (UUID String în MySQL)."""
    return db.query(m.User).filter(m.User.id == user_id).first()

def add_user(db: Session, user: m.User) -> m.User:
    """Persistă un obiect User nou în baza de date."""
    db.add(user)
    db.flush()
    db.refresh(user)
    return user

def create_password_reset(db: Session, reset_obj: m.PasswordReset):
    """Salvează cererea de resetare a parolei."""
    db.add(reset_obj)
    db.flush()
    return reset_obj