from sqlalchemy.orm import Session
from app.repository import message_repository as repo
from app.models import sql_models as m

class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, conversation_id: str, role: str, content: str):
        """Creează și persistă un obiect de tip Mesaj."""
        new_msg = m.Message(
            conversation_id=str(conversation_id),
            role=role,
            content=content
        )
        return repo.add(self.db, new_msg)

    def list_messages(self, conversation_id: str):
        """Obține lista de mesaje pentru o anumită conversație."""
        return repo.list_for_conversation(self.db, conversation_id)