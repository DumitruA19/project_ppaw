from typing import Iterable, Optional
from sqlalchemy.orm import Session
from app.models import sql_models as m

def list_for_user(db: Session, user_id: str) -> Iterable[m.Favorite]:
    return (
        db.query(m.Favorite)
        .filter(m.Favorite.user_id == str(user_id))
        .order_by(m.Favorite.created_at.desc())
        .all()
    )

def get_by_user_and_title(db: Session, user_id: str, title: str) -> Optional[m.Favorite]:
    return (
        db.query(m.Favorite)
        .filter(
            m.Favorite.user_id == str(user_id),
            m.Favorite.book_title == title,
        )
        .first()
    )

def add(db: Session, favorite: m.Favorite) -> m.Favorite:
    db.add(favorite)
    db.flush()
    db.refresh(favorite)
    return favorite

def delete(db: Session, favorite: m.Favorite) -> None:
    db.delete(favorite)
    db.flush()