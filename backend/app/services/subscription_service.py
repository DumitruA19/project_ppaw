# app/services/subscription_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.repository import subscription_repository, usage_repository
from app.models import sql_models as m
from app.utils.logger import log_event # Importăm utilitarul de logare

PLAN_LIMITS = {
    "FREE": 5,
    "STANDARD": 50,
    "PREMIUM": None 
}

class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db

    def create_subscription(self, user_id: str, plan_code: str):
        """Activează un plan nou și loghează tranziția."""
        plan_code = plan_code.upper()
        if plan_code not in PLAN_LIMITS:
            log_event(
                self.db, user_id, "SUB_CREATE_FAIL", "subscription/create", 
                f"Tentativă de activare plan invalid: {plan_code}", 
                status="ERROR"
            )
            raise ValueError("Plan invalid.")

        # 1. Anulează abonamentele vechi
        active = subscription_repository.get_active_for_user(self.db, user_id)
        if active:
            active.status = "canceled"
            log_event(self.db, user_id, "SUB_CANCELED", "subscription/create", f"Plan anterior ({active.plan_name}) anulat.")

        now = datetime.utcnow()
        # 2. Creează obiectul de abonament
        sub = m.Subscription(
            user_id=str(user_id),
            plan_name=plan_code, 
            status="active",
            current_period_start=now,
            current_period_end=now + timedelta(days=30)
        )
        self.db.add(sub)
        
        # 3. Inițializează contorul de consum
        usage = m.UsageCounter(
            user_id=str(user_id),
            period_start=sub.current_period_start.date(),
            period_end=sub.current_period_end.date(),
            messages_used=0
        )
        self.db.add(usage)
        self.db.commit()

        log_event(self.db, user_id, "SUB_ACTIVATED", "subscription/create", f"Plan nou activat: {plan_code}")
        return sub

    def consume_attempt(self, user_id: str):
        """Înregistrează consumul unui mesaj și loghează evenimentul."""
        sub = subscription_repository.get_active_for_user(self.db, user_id)
        if not sub:
            log_event(self.db, user_id, "USAGE_FAIL", "subscription/consume", "Consum eșuat: Utilizator fără abonament.", status="ERROR")
            raise ValueError("Nu există abonament activ.")

        usage = usage_repository.get_usage(
            self.db, user_id=str(user_id),
            period_start=sub.current_period_start.date(),
            period_end=sub.current_period_end.date()
        )

        limit = PLAN_LIMITS.get(sub.plan_name, 5) 
        if limit is not None and usage.messages_used >= limit:
            log_event(self.db, user_id, "SUB_LIMIT_REACHED", "subscription/consume", f"Limita atinsă pentru {sub.plan_name} ({limit} mesaje).", status="WARNING")
            raise ValueError("Limita maximă atinsă.")

        usage.messages_used += 1
        usage.last_update = datetime.utcnow()
        self.db.commit()
        
        log_event(self.db, user_id, "MESSAGE_CONSUMED", "subscription/consume", f"Mesaj contorizat. Total actual: {usage.messages_used}")

    def check_usage_limit(self, user_id: str):
        """Verifică limita de utilizare și loghează eventualele blocaje."""
        sub = subscription_repository.get_active_for_user(self.db, user_id)
        if not sub:
            log_event(self.db, user_id, "CHECK_LIMIT_FAIL", "subscription/check", "Verificare limită: Abonament inexistent.", status="ERROR")
            raise ValueError("Nu aveți un abonament activ. Vă rugăm să alegeți un plan.")

        usage = usage_repository.get_usage(
            self.db, user_id=str(user_id),
            period_start=sub.current_period_start.date(),
            period_end=sub.current_period_end.date()
        )

        if not usage:
            return True 

        limit = PLAN_LIMITS.get(sub.plan_name, 5)
        if limit is not None and usage.messages_used >= limit:
            log_event(self.db, user_id, "CHECK_LIMIT_BLOCKED", "subscription/check", f"Utilizator blocat: Limita de {limit} mesaje pentru {sub.plan_name} a fost atinsă.")
            raise ValueError(f"Ai consumat toate cele {limit} mesaje incluse în planul {sub.plan_name}.")
        
        return True
    
    def can_use_feature(self, user_id: str) -> bool:
        """Verificare rapidă pentru UI/Logică internă."""
        sub = subscription_repository.get_active_for_user(self.db, user_id)
        if not sub:
            return False

        usage = usage_repository.get_usage(
            self.db, user_id=str(user_id),
            period_start=sub.current_period_start.date(),
            period_end=sub.current_period_end.date()
        )

        if not usage:
            return True

        limit = PLAN_LIMITS.get(sub.plan_name, 5) 
        if limit is None: 
            return True
            
        is_allowed = usage.messages_used < limit
        if not is_allowed:
            log_event(self.db, user_id, "FEATURE_ACCESS_DENIED", "subscription/feature", f"Acces refuzat la feature (Limita atinsă: {sub.plan_name})")
        
        return is_allowed