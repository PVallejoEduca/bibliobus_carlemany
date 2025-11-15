from dataclasses import dataclass

from ..repositories.ratings_repo import RatingsRepository


@dataclass
class Recommendation:
    book_id: int
    title: str
    score: float
    ratings: int


class RecsService:
    """Calcula popularidad regularizada."""

    def __init__(self, repo: RatingsRepository):
        self.repo = repo

    def top_global(self, m: int) -> list[Recommendation]:
        stats = self._fetch_stats()
        if not stats:
            return []
        total_votes = sum(int(row.count) for row in stats) or 1
        weighted_sum = sum(int(row.count) * float(row.avg) for row in stats)
        global_avg = (weighted_sum / total_votes) if total_votes else 0.0
        recs = []
        for row in stats:
            count = int(row.count)
            avg = float(row.avg)
            denom = count + m
            score = ((count / denom) * avg) + ((m / denom) * global_avg)
            recs.append(Recommendation(book_id=row.book_id, title=row.title, score=round(score, 3), ratings=count))
        return recs

    def hidden_gems(self, min_votes: int, max_votes: int, min_avg: float) -> list[Recommendation]:
        stats = self._fetch_stats()
        gems: list[Recommendation] = []
        for row in stats:
            count = int(row.count)
            avg = float(row.avg)
            if count < min_votes or count > max_votes or avg < min_avg:
                continue
            gems.append(
                Recommendation(
                    book_id=row.book_id,
                    title=row.title,
                    score=round(avg, 2),
                    ratings=count,
                )
            )
        gems.sort(key=lambda r: r.score, reverse=True)
        return gems

    def _fetch_stats(self, limit: int | None = None):
        return list(self.repo.rating_stats(limit=limit))
