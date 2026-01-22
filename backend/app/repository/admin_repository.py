from sqlalchemy.orm import Session
from app.models import sql_models as m

def list_all_users(db: Session):
    """Obține toți utilizatorii ordonați după data creării."""
    return db.query(m.User).order_by(m.User.created_at.desc()).all()

def get_user_by_id(db: Session, user_id: str):
    """Căutare specifică după ID-ul de tip string (UUID)."""
    return db.query(m.User).filter(m.User.id == user_id).first()

def remove_user(db: Session, user: m.User):
    """Ștergere fizică din baza de date."""
    db.delete(user)
    db.flush()

def list_all_plans(db: Session):
    """Afișează toate planurile, inclusiv cele inactive, pentru admin."""
    return db.query(m.BillingPlan).order_by(m.BillingPlan.price_cents.asc()).all()

def get_plan_by_id(db: Session, plan_id: int):
    """Căutare plan după ID-ul întreg."""
    return db.query(m.BillingPlan).filter(m.BillingPlan.id == plan_id).first()

def save_plan(db: Session, plan: m.BillingPlan):
    """Adaugă sau actualizează un plan în sesiune."""
    db.add(plan)
    db.flush()
    return plan