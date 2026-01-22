from typing import Iterable, Optional
from sqlalchemy.orm import Session
from app.models import sql_models as m

def list_active(db: Session) -> Iterable[m.BillingPlan]:
    """Returnează toate planurile active din MySQL, ordonate după preț."""
    return (
        db.query(m.BillingPlan)
        .filter(m.BillingPlan.is_active.is_(True))
        .order_by(m.BillingPlan.price_cents.asc())
        .all()
    )

def get_by_id(db: Session, plan_id: int) -> Optional[m.BillingPlan]:
    """Caută un plan după ID-ul întreg (specific MySQL/SQL Server)."""
    return db.query(m.BillingPlan).filter(m.BillingPlan.id == plan_id).first()

def get_by_code(db: Session, code: str) -> Optional[m.BillingPlan]:
    """Căutare după codul unic al planului (ex: 'PREMIUM')."""
    return db.query(m.BillingPlan).filter(m.BillingPlan.code == code).first()

def add_subscription(db: Session, subscription: m.Subscription) -> m.Subscription:
    """Persistă noul abonament creat în urma simulării plății."""
    db.add(subscription)
    db.flush()
    db.refresh(subscription)
    return subscription