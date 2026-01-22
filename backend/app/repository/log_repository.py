from sqlalchemy.orm import Session
from app.models import sql_models as m

def add_log_entry(db: Session, log_obj: m.Log) -> m.Log:
    """Inserează o nouă intrare de log în baza de date MySQL."""
    db.add(log_obj)
    db.flush()
    db.refresh(log_obj)
    return log_obj

def list_logs(db: Session, limit: int = 100):
    """Recuperează ultimele log-uri pentru panoul de administrare."""
    return db.query(m.Log).order_by(m.Log.created_at.desc()).limit(limit).all()