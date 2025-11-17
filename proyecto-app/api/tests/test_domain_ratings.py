from types import SimpleNamespace

import pytest

from app.domain.kpis_service import KpisService
from app.domain.ratings_service import RatingsService


class DummyRepo:
    def __init__(self, users=None, copies=None, existing=None):
        self.users = users or set()
        self.copies = copies or set()
        self.existing = existing or set()
        self.created_payload = None

    def user_exists(self, user_id):
        return user_id in self.users

    def copy_exists(self, copy_id):
        return copy_id in self.copies

    def get_rating(self, user_id, copy_id):
        return (user_id, copy_id) in self.existing

    def create_rating(self, user_id, copy_id, rating, comment):
        self.created_payload = (user_id, copy_id, rating, comment)
        return SimpleNamespace(
            rating_id=99,
            user_id=user_id,
            copy_id=copy_id,
            rating=rating,
            comment=comment,
        )

    def kpi_counts(self):
        return {"books": 2}


def test_add_rating_success():
    repo = DummyRepo(users={1}, copies={10})
    service = RatingsService(repo)

    result = service.add_rating(1, 10, 4, "bien")

    assert result["rating_id"] == 99
    assert repo.created_payload == (1, 10, 4, "bien")


@pytest.mark.parametrize(
    "payload,error",
    [
        ((1, 10, 0), "rating_fuera_de_rango"),
        ((1, 10, 6), "rating_fuera_de_rango"),
    ],
)
def test_add_rating_invalid_range(payload, error):
    repo = DummyRepo(users={1}, copies={10})
    service = RatingsService(repo)
    with pytest.raises(ValueError, match=error):
        service.add_rating(payload[0], payload[1], payload[2])


def test_add_rating_checks_user_and_copy():
    repo = DummyRepo(users=set(), copies=set())
    service = RatingsService(repo)
    with pytest.raises(ValueError, match="user_inexistente"):
        service.add_rating(99, 10, 4)

    repo.users.add(99)
    with pytest.raises(ValueError, match="copy_inexistente"):
        service.add_rating(99, 10, 4)


def test_add_rating_detects_duplicates():
    repo = DummyRepo(users={1}, copies={2}, existing={(1, 2)})
    service = RatingsService(repo)
    with pytest.raises(ValueError, match="rating_duplicado"):
        service.add_rating(1, 2, 5)


def test_kpis_service_returns_counts():
    repo = DummyRepo()
    service = KpisService(repo)
    assert service.get_kpis() == {"books": 2}
