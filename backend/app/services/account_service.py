
from sqlalchemy.orm import Session
from app.repository import account_repository as repo
from app.core.security import verify_password, hash_password
from datetime import date
import calendar

# Importuri pentru funcționalități și logare
from app.repository import subscription_repository, usage_repository
from app.services.subscription_service import PLAN_LIMITS
from app.utils.logger import log_event # Utilitarul creat anterior

class AccountService:
    def __init__(self, db: Session):
        self.db = db

    def get_profile(self, user):
        """Formatează datele profilului și loghează accesul."""
        log_event(
            self.db, user.id, "PROFILE_VIEW", "/account/me", 
            f"Utilizatorul {user.email} și-a accesat datele de profil."
        )
        
        return {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }

    def change_password(self, user, old_password: str, new_password: str):
        """Validează parola veche, o actualizează și loghează rezultatul."""
        if not verify_password(old_password, user.password_hash):
            log_event(
                self.db, user.id, "SECURITY_FAILURE", "/account/password", 
                "Tentativă eșuată de schimbare a parolei (parola veche incorectă).",
                status="ERROR"
            )
            raise ValueError("Parola curentă este incorectă.")

        user.password_hash = hash_password(new_password)
        self.db.add(user) # Adăugăm obiectul pentru a marca modificarea
        self.db.commit()
        
        return {"message": "Parola a fost actualizată cu succes."}

    def get_overview(self, user):
        """Obține datele despre abonament și loghează vizualizarea consumului."""
        sub = subscription_repository.get_active_for_user(self.db, user.id)
        
        usage_data = {"used": 0, "limit": 5} 
        
        if sub:
            usage = usage_repository.get_usage(
                self.db, 
                user_id=str(user.id),
                period_start=sub.current_period_start.date(),
                period_end=sub.current_period_end.date()
            )
            
            usage_data = {
                "used": usage.messages_used if usage else 0,
                "limit": PLAN_LIMITS.get(sub.plan_name, 5) 
            }

        log_event(
            self.db, user.id, "ACCOUNT_OVERVIEW", "/account/overview", 
            f"Vizualizare stare abonament ({sub.plan_name if sub else 'FREE'}). Consum: {usage_data['used']}/{usage_data['limit']}."
        )

        return {
            "subscription": {
                "plan": sub.plan_name if sub else "FREE",
                "status": sub.status if sub else "inactive",
                "messages_used": usage_data["used"],
                "messages_limit": usage_data["limit"],
                "current_period_end": sub.current_period_end if sub else None
            }
        }