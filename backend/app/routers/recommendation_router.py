from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import schema as s
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Book Recommendations"])

@router.get("/{conversation_id}", response_model=list[s.RecommendationOut])
def list_recommendations(conversation_id: str, db: Session = Depends(get_db)):
    """Punct de acces pentru vizualizarea cărților recomandate într-o conversație."""
    service = RecommendationService(db)
    return service.list_for_conversation(conversation_id)