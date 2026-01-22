# app/repository/usage_repository.py
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from app.models import sql_models as m

def get_usage( # Redenumit pentru a se potrivi cu Service-ul
    db: Session,
    user_id: str,
    period_start: date,
    period_end: date,
) -> Optional[m.UsageCounter]:
    return (
        db.query(m.UsageCounter)
        .filter(
            m.UsageCounter.user_id == str(user_id),
            m.UsageCounter.period_start == period_start,
            m.UsageCounter.period_end == period_end,
        )
        .first()
    )

def save_usage(db: Session, usage: m.UsageCounter) -> m.UsageCounter:
    db.add(usage)
    db.commit() # Folosește commit pentru a salva în MySQL
    db.refresh(usage)
    return usage