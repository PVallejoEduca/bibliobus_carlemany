from types import SimpleNamespace

import pytest

from app.domain.recs_service import RecsService


class FakeRepo:
    def __init__(self, stats):
        self._stats = stats

    def rating_stats(self, limit=None):
        return self._stats


def make_row(book_id, title, count, avg):
    return SimpleNamespace(book_id=book_id, title=title, count=count, avg=avg)


def test_top_global_returns_weighted_scores():
    repo = FakeRepo(
        [
            make_row(1, "Libro Uno", 10, 4.0),
            make_row(2, "Libro Dos", 5, 5.0),
        ]
    )
    service = RecsService(repo)

    recs = service.top_global(m=5)

    assert len(recs) == 2
    assert recs[0].book_id == 1  # más votos, mayor score ponderado
    assert recs[1].score > 0


def test_top_global_empty_stats_returns_empty_list():
    service = RecsService(FakeRepo([]))
    assert service.top_global(m=5) == []


def test_hidden_gems_filters_by_votes_and_avg():
    repo = FakeRepo(
        [
            make_row(1, "Popular", 50, 4.5),
            make_row(2, "Rara", 8, 4.8),
            make_row(3, "Normal", 5, 3.0),
        ]
    )
    service = RecsService(repo)

    gems = service.hidden_gems(min_votes=3, max_votes=10, min_avg=4.0)

    assert [g.book_id for g in gems] == [2]
    assert gems[0].score == 4.8
