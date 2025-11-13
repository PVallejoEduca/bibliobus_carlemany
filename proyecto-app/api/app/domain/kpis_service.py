from ..repositories.ratings_repo import RatingsRepository


class KpisService:
    """Calcula KPIs basicos."""

    def __init__(self, repo: RatingsRepository):
        self.repo = repo

    def get_kpis(self) -> dict:
        return self.repo.kpi_counts()
