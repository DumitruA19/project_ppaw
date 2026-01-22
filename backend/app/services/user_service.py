from sqlalchemy.orm import Session
from app.repository import user_repository as repo
from app.models import sql_models as m
from app.core.security import hash_password
from app.utils.logger import log_event #

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def list_users(self):
        return repo.list_users(self.db)

    def get_user(self, user_id: str):
        return repo.get_by_id(self.db, user_id)

    def create_user(self, data: dict):
        email = data.get("email")
        if repo.get_by_email(self.db, email):
            log_event(self.db, None, "USER_CREATE_FAIL", "user/create", f"Email deja existent: {email}", status="ERROR")
            raise ValueError("Emailul este deja înregistrat.")
        
        if "password" in data:
            data["password_hash"] = hash_password(data.pop("password"))
            
        user = m.User(**data)
        result = repo.add(self.db, user)
        self.db.commit()
        log_event(self.db, result.id, "USER_CREATE_SUCCESS", "user/create", f"Utilizator nou creat: {email}")
        return result

    def delete_user(self, user_id: str):
        user = repo.get_by_id(self.db, user_id)
        if not user:
            log_event(self.db, None, "USER_DELETE_FAIL", "user/delete", f"ID inexistent: {user_id}", status="ERROR")
            raise ValueError("Utilizatorul nu a fost găsit.")
        repo.delete(self.db, user)
        self.db.commit()
        log_event(self.db, None, "USER_DELETE_SUCCESS", "user/delete", f"Utilizator șters: {user_id}")