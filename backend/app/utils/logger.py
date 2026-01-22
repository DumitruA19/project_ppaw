from sqlalchemy.orm import Session
from app.models.sql_models import ActionLog

def log_event(db: Session, user_id: str | None, action_type: str, endpoint: str, description: str, status: str = "SUCCESS"):
    """Înregistrează o activitate în baza de date MySQL."""
    try:
        new_log = ActionLog(
            user_id=str(user_id) if user_id else None,
            action_type=action_type,
            endpoint=endpoint,
            description=description,
            status=status
        )
        db.add(new_log)
        db.commit()
    except Exception as e:
        print(f"[CRITICAL] Failed to write log: {e}")