# app/core/dependencies.py  (corect)
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import sql_models as m

def check_subscription_active(user_id, db: Session) -> bool:
    sub = db.query(m.Subscription).filter(
        m.Subscription.user_id == user_id,
        m.Subscription.status.in_(["active", "trialing"]),
        m.Subscription.current_period_end > datetime.utcnow(),
    ).first()
    return sub is not None

def ensure_active_subscription_or_raise(user_id, db: Session):
    if not check_subscription_active(user_id, db):
        raise HTTPException(status_code=403, detail="Inactive subscription")
