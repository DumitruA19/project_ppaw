from sqlalchemy.orm import Session
from app.repository import recommendation_repository as repo
from app.models import sql_models as m

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def add_recommendation(self, conversation_id: str, book_title: str, reason: str = None, chroma_id: str = None):
        """Creează o înregistrare pentru o carte recomandată de AI."""
        recommendation = m.Recommendation(
            conversation_id=str(conversation_id),
            book_title=book_title,
            reason=reason,
            chroma_doc_id=chroma_id
        )
        return repo.add(self.db, recommendation)

    def list_for_conversation(self, conversation_id: str):
        """Returnează lista de sugestii pentru o sesiune de chat specifică."""
        return repo.list_for_conversation(self.db, conversation_id)