from sqlalchemy.orm import Session
from app.repository import admin_repository as repo
from app.core.security import hash_password
from app.models.sql_models import BillingPlan
from app.repository import subscription_repository
from app.utils.logger import log_event # Utilitarul pentru logare
from app.models import sql_models as m
# app/services/admin_service.py
from app.models.sql_models import ActionLog  # <--- Aceasta este linia critică
import json

class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def list_users(self, admin_id: str = None):
        # Luăm utilizatorii din baza de date
        users = repo.list_all_users(self.db)
        
        result = []
        for user in users:
            # Verificăm dacă utilizatorul are un abonament "active" în MySQL
            sub = subscription_repository.get_active_for_user(self.db, user.id)
            
            result.append({
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "has_active_plan": sub is not None and sub.status == "active" # <--- ACESTA ESTE CHEIA
            })
        
        # Logăm vizualizarea
        log_event(self.db, admin_id, "ADMIN_VIEW", "/admin/users", f"Accesare lista: {len(result)} useri")
        return result

    def update_user(self, user_id: str, data: dict, admin_id: str = None):
        """Actualizează selectiv datele utilizatorului și loghează acțiunea."""
        user = repo.get_user_by_id(self.db, user_id)
        if not user:
            raise ValueError("Utilizatorul nu a fost găsit.")

        # Actualizare câmpuri primite din frontend
        if "name" in data: user.name = data["name"]
        if "role" in data: user.role = data["role"]
        
        # Procesare parolă nouă (dacă este completată în modal)
        if "password" in data and data["password"]:
            user.password_hash = hash_password(data["password"])

        self.db.commit()
        
        # Înregistrarea acțiunii în Audit Logs
        log_event(
            self.db, admin_id, "ADMIN_USER_UPDATE_SUCCESS", "/admin/users/update", 
            f"Admin-ul a modificat datele pentru: {user.email}"
        )
        return user

    # app/services/admin_service.py

    def delete_user(self, user_id: str, admin_id: str = None):
        """Șterge un utilizator și loghează acțiunea."""
        user = repo.get_user_by_id(self.db, user_id)
        if not user:
            log_event(
                self.db, admin_id, "ADMIN_USER_DELETE_FAIL", "/admin/users/delete", 
                f"Eșec la ștergere. ID-ul {user_id} nu a fost găsit.", 
                status="ERROR"
            )
            raise ValueError("Utilizatorul nu a fost găsit.")
        
        # 🛡️ PROTECȚIE SUPLIMENTARĂ: Nu lăsa un admin să își șteargă propriul cont accidental
        # (Presupunem că 'admin_id' vine din token-ul de login)
        
        email_deleted = user.email
        repo.remove_user(self.db, user) #
        self.db.commit()
        
        log_event(
            self.db, admin_id, "ADMIN_USER_DELETE_SUCCESS", "/admin/users/delete", 
            f"Utilizatorul {email_deleted} (ID: {user_id}) a fost eliminat definitiv din sistem."
        )
        return {"message": "Utilizator șters cu succes."}

    def create_billing_plan(self, data: dict, admin_id: str = None):
        """Creează un plan nou și loghează detaliile acestuia."""
        try:
            new_plan = BillingPlan(
                code=data["code"],
                name=data["name"],
                period=data.get("period", "month"),
                price_cents=int(data["price_cents"]),
                currency=data.get("currency", "EUR"),
                limits_json=json.dumps(data.get("limits", {})),
                features_json=json.dumps(data.get("features", {})),
                is_active=True
            )
            repo.save_plan(self.db, new_plan)
            self.db.commit()
            
            log_event(
                self.db, admin_id, "ADMIN_PLAN_CREATE", "/admin/plans/create", 
                f"Plan tarifar nou creat: {data['name']} ({data['code']})."
            )
            return new_plan
        except Exception as e:
            log_event(
                self.db, admin_id, "ADMIN_PLAN_CREATE_FAIL", "/admin/plans/create", 
                f"Eroare la crearea planului: {str(e)}", 
                status="ERROR"
            )
            raise e

    def deactivate_billing_plan(self, plan_id: int, admin_id: str = None):
        """Dezactivează un plan și loghează modificarea."""
        plan = repo.get_plan_by_id(self.db, plan_id)
        if not plan:
            log_event(
                self.db, admin_id, "ADMIN_PLAN_DEACTIVATE_FAIL", "/admin/plans/deactivate", 
                f"Planul cu ID {plan_id} nu există.", 
                status="ERROR"
            )
            raise ValueError("Planul nu există.")
        
        plan.is_active = False
        self.db.commit()
        
        log_event(
            self.db, admin_id, "ADMIN_PLAN_DEACTIVATE", "/admin/plans/deactivate", 
            f"Planul '{plan.name}' (ID: {plan_id}) a fost dezactivat."
        )
        return {"message": f"Planul {plan.name} a fost dezactivat."}
    
    def get_logs(self, limit: int = 100):
            """Extrage ultimele 100 de acțiuni din sistem."""
            # Această linie cauza eroarea 500
            return self.db.query(ActionLog).order_by(ActionLog.created_at.desc()).limit(limit).all()
        
    
    def create_user(self, data: dict, admin_id: str = None):
        """Creează un utilizator nou din interfața de admin."""
        # Fără importul de mai sus, linia de mai jos generează NameError
        if self.db.query(m.User).filter(m.User.email == data["email"]).first():
            raise ValueError("Emailul este deja înregistrat.")
            
        new_user = m.User(
            email=data["email"],
            name=data.get("name"),
            password_hash=hash_password(data["password"]),
            role=data.get("role", "user")
        )
        self.db.add(new_user)
        self.db.commit()
        
        log_event(self.db, admin_id, "ADMIN_USER_CREATE", "/admin/users", f"Admin creat user: {data['email']}")
        return new_user
    
    def list_users(self, admin_id: str = None):
        users = repo.list_all_users(self.db)
        result = []
        
        for user in users:
            # Obținem abonamentul activ din repository
            sub = subscription_repository.get_active_for_user(self.db, user.id)
            
            result.append({
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                # ✅ REPARARE: Trimitem ambele câmpuri cerute de Frontend
                "has_active_plan": sub is not None and sub.status == "active",
                "plan_name": sub.plan_name if sub else "Niciunul"
            })
        
        log_event(self.db, admin_id, "ADMIN_VIEW", "/admin/users", f"Accesare lista: {len(result)} useri")
        return result