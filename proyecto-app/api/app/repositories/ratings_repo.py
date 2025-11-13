from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from .. import models


class RatingsRepository:
    """Encapsulates rating queries."""

    def __init__(self, session: Session):
        self.session = session

    def get_rating(self, user_id: int, copy_id: int):
        stmt = select(models.Rating).where(
            models.Rating.user_id == user_id,
            models.Rating.copy_id == copy_id,
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def copy_exists(self, copy_id: int) -> bool:
        return self.session.get(models.Copy, copy_id) is not None

    def user_exists(self, user_id: int) -> bool:
        return self.session.get(models.User, user_id) is not None

    def create_rating(self, user_id: int, copy_id: int, rating: int):
        rating_obj = models.Rating(user_id=user_id, copy_id=copy_id, rating=rating)
        self.session.add(rating_obj)
        self.session.flush()
        return rating_obj

    def list_ratings(self, book_id: int | None = None, user_id: int | None = None):
        stmt: Select = select(models.Rating).order_by(models.Rating.rating_id.desc())
        if book_id is not None:
            stmt = (
                stmt.join(models.Copy)
                .where(models.Copy.book_id == book_id)
            )
        if user_id is not None:
            stmt = stmt.where(models.Rating.user_id == user_id)
        return list(self.session.scalars(stmt))

    def kpi_counts(self):
        counts = {
            "books": self.session.execute(select(func.count(models.Book.book_id))).scalar_one(),
            "copies": self.session.execute(select(func.count(models.Copy.copy_id))).scalar_one(),
            "users": self.session.execute(select(func.count(models.User.user_id))).scalar_one(),
            "ratings": self.session.execute(select(func.count(models.Rating.rating_id))).scalar_one(),
        }
        orphan_copies_stmt = (
            select(func.count(models.Copy.copy_id))
            .outerjoin(models.Book, models.Copy.book_id == models.Book.book_id)
            .where(models.Book.book_id.is_(None))
        )
        orphan_ratings_stmt = (
            select(func.count(models.Rating.rating_id))
            .outerjoin(models.Copy, models.Rating.copy_id == models.Copy.copy_id)
            .where(models.Copy.copy_id.is_(None))
        )
        counts["orphan_copies"] = self.session.execute(orphan_copies_stmt).scalar_one()
        counts["orphan_ratings"] = self.session.execute(orphan_ratings_stmt).scalar_one()
        return counts

    def rating_stats(self):
        stmt = (
            select(
                models.Book.book_id,
                models.Book.title,
                func.count(models.Rating.rating_id).label("count"),
                func.avg(models.Rating.rating).label("avg"),
            )
            .join(models.Copy, models.Copy.book_id == models.Book.book_id)
            .join(models.Rating, models.Rating.copy_id == models.Copy.copy_id)
            .group_by(models.Book.book_id, models.Book.title)
            .order_by(func.count(models.Rating.rating_id).desc())
        )
        return self.session.execute(stmt).all()
