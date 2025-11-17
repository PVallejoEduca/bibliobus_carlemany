from app.repositories.ratings_repo import RatingsRepository


def test_kpi_counts_match_seed_dataset(db_session):
    repo = RatingsRepository(db_session)
    kpis = repo.kpi_counts()
    assert kpis["books"] == 2
    assert kpis["copies"] == 3
    assert kpis["users"] == 2
    assert kpis["ratings"] == 3
    assert kpis["avg_copies_per_book"] == 1.5
    assert kpis["avg_ratings_per_user"] == 1.5
    assert kpis["avg_ratings_per_book"] == 1.5


def test_data_quality_error_rate_under_threshold(db_session):
    repo = RatingsRepository(db_session)
    kpis = repo.kpi_counts()
    total_entities = kpis["copies"] + kpis["ratings"]
    errors = kpis["orphan_copies"] + kpis["orphan_ratings"]
    error_rate = errors / total_entities if total_entities else 0
    assert error_rate < 0.005
