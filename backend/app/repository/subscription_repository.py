from typing import Iterable, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import sql_models as m

def get_by_id(db: Session, sub_id: int) -> Optional[m.Subscription]:
    return db.query(m.Subscription).filter(m.Subscription.id == sub_id).first()

def get_active_for_user(db: Session, user_id: str) -> Optional[m.Subscription]:
    """Identifică abonamentul curent utilizabil."""
    return (
        db.query(m.Subscription)
        .filter(
            m.Subscription.user_id == str(user_id),
            m.Subscription.status.in_(("trialing", "active")),
            m.Subscription.current_period_end > datetime.utcnow()
        )
        .first()
    )

def add(db: Session, sub: m.Subscription) -> m.Subscription:
    db.add(sub)
    db.flush()
    db.refresh(sub)
    return sub