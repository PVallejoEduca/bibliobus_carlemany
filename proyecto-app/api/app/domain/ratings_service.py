from ..repositories.ratings_repo import RatingsRepository


class RatingsService:
    """Valida y crea valoraciones."""

    def __init__(self, repo: RatingsRepository):
        self.repo = repo

    def add_rating(self, user_id: int, copy_id: int, rating: int):
        if rating < 1 or rating > 5:
            raise ValueError("rating_fuera_de_rango")
        if not self.repo.user_exists(user_id):
            raise ValueError("user_inexistente")
        if not self.repo.copy_exists(copy_id):
            raise ValueError("copy_inexistente")
        if self.repo.get_rating(user_id, copy_id):
            raise ValueError("rating_duplicado")
        rating_obj = self.repo.create_rating(user_id, copy_id, rating)
        return {
            "rating_id": rating_obj.rating_id,
            "user_id": rating_obj.user_id,
            "copy_id": rating_obj.copy_id,
            "rating": rating_obj.rating,
        }

    def list_ratings(self, book_id: int | None = None, user_id: int | None = None):
        ratings = self.repo.list_ratings(book_id=book_id, user_id=user_id)
        return [
            {
                "rating_id": r.rating_id,
                "user_id": r.user_id,
                "copy_id": r.copy_id,
                "rating": r.rating,
            }
            for r in ratings
        ]
