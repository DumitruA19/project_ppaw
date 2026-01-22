# backend/seed_plans.py

from sqlalchemy.orm import Session
from core.db import SessionLocal
from models.subscriptions import BillingPlan

def seed():
    db: Session = SessionLocal()
    plans = [
        {
            "code": "free",
            "name": "Free",
            "price_cents": 0,
            "period": "month",
            "limits_json": '{"monthly_messages": 30, "tts": false}',
            "features_json": '{"basic_access": true}',
        },
        {
            "code": "trial",
            "name": "Trial",
            "price_cents": 0,
            "period": "month",
            "limits_json": '{"monthly_messages": 100, "tts": true}',
            "features_json": '{"trial_access": true}',
        },
        {
            "code": "premium",
            "name": "Premium",
            "price_cents": 999,
            "period": "month",
            "limits_json": '{"monthly_messages": 1000, "tts": true}',
            "features_json": '{"premium_access": true}',
        },
    ]

    for p in plans:
        plan = BillingPlan(**p)
        db.add(plan)
    db.commit()
    print("Billing plans seeded.")


if __name__ == "__main__":
    seed()
