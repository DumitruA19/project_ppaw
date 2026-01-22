# app/services/billing_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.repository import billing_repository as repo
from app.models import sql_models as m
from app.utils.logger import log_event # Importăm utilitarul de logare

class BillingService:
    def __init__(self, db: Session):
        self.db = db

    def list_active_plans(self, user_id: str = None):
        """Obține lista planurilor și loghează vizualizarea acestora."""
        log_event(
            self.db, user_id, "BILLING_PLANS_VIEW", "/plans", 
            "Utilizatorul a vizualizat oferta de planuri tarifare."
        )
        return repo.list_active(self.db)

    def simulate_subscription(self, user_id: str, plan_code: str):
        """
        Simulează procesul de plată și loghează succesul sau eșecul tranzacției.
        """
        plan = repo.get_by_code(self.db, plan_code)
        
        if not plan:
            # Logăm eșecul tranzacției dacă planul nu este valid
            log_event(
                self.db, user_id, "BILLING_SUB_FAIL", "/subscriptions/checkout", 
                f"Tentativă de abonare eșuată. Planul '{plan_code}' nu a fost găsit.", 
                status="ERROR"
            )
            raise ValueError("Planul specificat nu există.")

        now = datetime.utcnow()
        # Creăm obiectul de abonament (simulăm succesul plății)
        new_sub = m.Subscription(
            user_id=user_id,
            plan_id=plan.id,
            provider="simulated_payment",
            status="active",
            current_period_start=now,
            current_period_end=now + timedelta(days=30)
        )
        
        try:
            repo.add_subscription(self.db, new_sub)
            self.db.commit()
            
            # Logăm activarea cu succes a noului abonament
            log_event(
                self.db, user_id, "BILLING_SUB_SUCCESS", "/subscriptions/checkout", 
                f"Abonament activat cu succes pentru planul: {plan.name} ({plan_code})."
            )
            return new_sub
            
        except Exception as e:
            self.db.rollback()
            log_event(
                self.db, user_id, "BILLING_DB_ERROR", "/subscriptions/checkout", 
                f"Eroare la salvarea abonamentului în baza de date: {str(e)}", 
                status="ERROR"
            )
            raise e