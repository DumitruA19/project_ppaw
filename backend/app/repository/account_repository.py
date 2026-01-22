from sqlalchemy.orm import Session
from app.models import sql_models as m
from datetime import date

def get_user_by_id(db: Session, user_id: str):
    """Returnează utilizatorul după ID."""
    return db.query(m.User).filter(m.User.id == user_id).first()

def get_active_subscription(db: Session, user_id: str):
    """Caută un abonament activ sau în trial pentru utilizator."""
    return db.query(m.Subscription).filter(
        m.Subscription.user_id == user_id,
        m.Subscription.status.in_(["active", "trialing"])
    ).order_by(m.Subscription.current_period_end.desc()).first()

def get_current_usage(db: Session, user_id: str, start_date: date, end_date: date):
    """Returnează contorul de utilizare pentru perioada specificată."""
    return db.query(m.UsageCounter).filter(
        m.UsageCounter.user_id == user_id,
        m.UsageCounter.period_start == start_date,
        m.UsageCounter.period_end == end_date
    ).first()