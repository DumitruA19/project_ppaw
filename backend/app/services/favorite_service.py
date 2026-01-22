from sqlalchemy.orm import Session
from app.repository import favorite_repository as repo
from app.models import sql_models as m

class FavoriteService:
    def __init__(self, db: Session):
        self.db = db

    def list_user_favorites(self, user_id: str):
        return repo.list_for_user(self.db, user_id)

    def add_favorite(self, user_id: str, title: str):
        existing = repo.get_by_user_and_title(self.db, user_id, title)
        if existing:
            raise ValueError("Această carte este deja în lista de favorite.") #
        
        favorite = m.Favorite(user_id=str(user_id), book_title=title)
        repo.add(self.db, favorite)
        self.db.commit()
        return favorite

    def remove_favorite(self, user_id: str, title: str):
        favorite = repo.get_by_user_and_title(self.db, user_id, title)
        if not favorite:
            raise ValueError("Cartea nu a fost găsită în favorite.") #
        
        repo.delete(self.db, favorite)
        self.db.commit()