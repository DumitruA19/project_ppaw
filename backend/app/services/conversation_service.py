from sqlalchemy.orm import Session
from app.repository import conversation_repository as repo
from app.models import sql_models as m

class ConversationService:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, user_id: str, title: str = None):
        """Inițializează o sesiune nouă de chat."""
        new_conv = m.Conversation(user_id=str(user_id), title=title)
        return repo.add(self.db, new_conv)

    def get_conversation(self, conversation_id: str):
        """Recuperează o conversație specifică; aruncă eroare dacă nu există."""
        conv = repo.get_by_id(self.db, conversation_id)
        if not conv:
            raise ValueError("Conversația nu a fost găsită.")
        return conv

    def list_user_conversations(self, user_id: str):
        """Obține toate sesiunile de chat ale utilizatorului."""
        return repo.list_for_user(self.db, user_id)