from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import get_current_user
from app.models import schema as s
from app.services.favorite_service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["Favorites Management"])

@router.get("/", response_model=list[s.FavoriteOut])
def get_my_favorites(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return FavoriteService(db).list_user_favorites(current_user.id)

@router.post("/", response_model=s.FavoriteOut, status_code=status.HTTP_201_CREATED)
def mark_as_favorite(data: s.FavoriteCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return FavoriteService(db).add_favorite(current_user.id, data.book_title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{title}")
def unmark_favorite(title: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        FavoriteService(db).remove_favorite(current_user.id, title)
        return {"detail": "Cartea a fost eliminată din favorite."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))