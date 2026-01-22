# app/services/usage_service.py
from sqlalchemy.orm import Session
from app.repository import usage_repository as repo
from app.models import sql_models as m
from datetime import date
from app.utils.logger import log_event  # Importăm utilitarul de logare

class UsageService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_usage(self, user_id: str, start: date, end: date):
        """Returnează datele de consum și loghează interogarea."""
        log_event(
            self.db, user_id, "USAGE_VIEW", "usage/get",
            f"S-au extras datele de consum pentru perioada {start} - {end}."
        )
        return repo.get_usage_record(self.db, str(user_id), start, end)

    def create_usage_entry(self, data: dict):
        """Creează un obiect UsageCounter și loghează inițializarea acestuia."""
        user_id = data.get("user_id")
        try:
            usage = m.UsageCounter(**data)
            result = repo.save_usage(self.db, usage)
            self.db.commit()

            # Logăm succesul inițializării contorului
            log_event(
                self.db, user_id, "USAGE_INIT_SUCCESS", "usage/create",
                f"Contor nou de consum creat pentru perioada {data.get('period_start')} - {data.get('period_end')}."
            )
            return result
            
        except Exception as e:
            self.db.rollback()
            # Logăm eșecul salvării în baza de date
            log_event(
                self.db, user_id, "USAGE_INIT_ERROR", "usage/create",
                f"Eroare la inițializarea contorului de consum: {str(e)}",
                status="ERROR"
            )
            raise e