from sqlalchemy.orm import Session
from app.repository import log_repository as repo
from app.models import sql_models as m
import json

class LogService:
    def __init__(self, db: Session):
        self.db = db

    def log_event(self, action: str, user_id: str = None, metadata: dict = None, meta: str = None):
        """
        Înregistrează un eveniment. 
        Converteste metadatele (dict) în format string pentru stocare în MySQL.
        """
        log_entry = m.Log(
            user_id=str(user_id) if user_id else None,
            action=action,
            metadata_json=json.dumps(metadata) if metadata else None,
            meta=meta
        )
        return repo.add_log_entry(self.db, log_entry)