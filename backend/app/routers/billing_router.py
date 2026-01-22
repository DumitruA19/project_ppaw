from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import get_current_user
from app.services.billing_service import BillingService
from app.models import schema as s

router = APIRouter(prefix="/billing", tags=["Billing & Subscriptions"])

@router.get("/plans")
def get_plans(db: Session = Depends(get_db)):
    """Returnează planurile de tarifare disponibile."""
    # Simulare listă planuri sau interogare db.query(m.BillingPlan).all()
    return [
        {"name": "FREE", "price": 0, "limit": 5},
        {"name": "STANDARD", "price": 29, "limit": 50},
        {"name": "PREMIUM", "price": 99, "limit": None}
    ]

@router.post("/subscribe/{plan_code}")
def subscribe_to_plan(
    plan_code: str, 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    """Endpoint pentru simularea unei plăți și activarea unui plan."""
    try:
        service = BillingService(db)
        return service.simulate_subscription(str(user.id), plan_code.upper())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))