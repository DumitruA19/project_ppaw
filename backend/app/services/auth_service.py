from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import uuid4

from app.repository import auth_repository as repo
from app.models import sql_models as m
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.logger import log_event  # Importăm utilitarul de logare

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, email: str, name: str, password: str, role: str = "user"):
        """Gestionează crearea unui cont nou și loghează succesul sau eșecul."""
        if repo.get_by_email(self.db, email):
            # Logăm tentativa eșuată de înregistrare
            log_event(
                self.db, None, "AUTH_REGISTER_FAIL", "/auth/register", 
                f"Tentativă de înregistrare cu email existent: {email}", 
                status="ERROR"
            )
            raise HTTPException(status_code=400, detail="Emailul este deja folosit.")

        new_user = m.User(
            email=email,
            name=name,
            password_hash=hash_password(password),
            role=role
        )
        repo.add_user(self.db, new_user)
        self.db.commit()

        # Logăm succesul înregistrării
        log_event(
            self.db, new_user.id, "AUTH_REGISTER_SUCCESS", "/auth/register", 
            f"Utilizator nou creat cu succes: {email}"
        )
        return new_user

    def login(self, email: str, password: str):
        """Verifică credențialele, generează token-ul și loghează activitatea."""
        user = repo.get_by_email(self.db, email)
        
        if not user or not verify_password(password, user.password_hash):
            # Logăm eșecul autentificării (posibil atac brute-force sau greșeală)
            log_event(
                self.db, None, "AUTH_LOGIN_FAIL", "/auth/login", 
                f"Eșec autentificare pentru email: {email}", 
                status="ERROR"
            )
            raise HTTPException(status_code=401, detail="Email sau parolă incorectă.")

        token = create_access_token(sub=str(user.id), role=user.role)
        
        # Logăm succesul logării
        log_event(
            self.db, user.id, "AUTH_LOGIN_SUCCESS", "/auth/login", 
            f"Utilizatorul {email} s-a logat cu succes."
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "role": user.role
        }

    def start_reset(self, email: str):
        """Generează un token de resetare și loghează cererea."""
        user = repo.get_by_email(self.db, email)
        
        if not user:
            # Logăm cererea pentru un email care nu există în sistem
            log_event(
                self.db, None, "AUTH_RESET_FAIL", "/auth/reset", 
                f"Cerere resetare parolă pentru email inexistent: {email}", 
                status="ERROR"
            )
            raise HTTPException(status_code=404, detail="Utilizator inexistent.")

        reset = m.PasswordReset(
            user_id=user.id,
            token=str(uuid4()),
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        repo.create_password_reset(self.db, reset)
        self.db.commit()

        # Logăm generarea token-ului de resetare
        log_event(
            self.db, user.id, "AUTH_RESET_START", "/auth/reset", 
            f"A fost generat un token de resetare a parolei pentru: {email}"
        )
        
        return {"message": "Token generat.", "token": reset.token}