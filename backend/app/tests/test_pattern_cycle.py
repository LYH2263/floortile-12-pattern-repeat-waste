import pytest
from fastapi import HTTPException

from app.engines.tile_math import tile_count


def test_cycle_zero_matches_base_order():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, pattern_cycle=0.0)
    assert r["pattern_cycle"] == 0.0
    assert r["pattern_cycles"] == 0
    assert r["pattern_extra"] == 0
    assert r["order_count"] == r["base_order_count"] == 81


def test_cycle_adds_matching_extra():
    # cycles=ceil(6/2)=3, per_row=10, matched=3*ceil(2/0.6)=12, rows=8 -> extra 16
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, pattern_cycle=2.0)
    assert r["pattern_cycles"] == 3
    assert r["pattern_extra"] == 16
    assert r["base_order_count"] == 81
    assert r["order_count"] == 97


def test_cycle_exact_fit_no_extra():
    # tile divides the cycle evenly: 5 cycles * 2 tiles = 10 = plain per-row count
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, pattern_cycle=1.2)
    assert r["pattern_cycles"] == 5
    assert r["pattern_extra"] == 0
    assert r["order_count"] == r["base_order_count"]


def test_cycle_equal_room_length_fails():
    with pytest.raises(ValueError):
        tile_count(6.0, 4.5, 0.6, 0.6, 8.0, pattern_cycle=6.0)


def test_cycle_longer_than_room_fails():
    with pytest.raises(ValueError):
        tile_count(6.0, 4.5, 0.6, 0.6, 8.0, pattern_cycle=7.5)


def test_cycle_negative_fails():
    with pytest.raises(ValueError):
        tile_count(6.0, 4.5, 0.6, 0.6, 8.0, pattern_cycle=-1.0)


@pytest.fixture()
def fresh_db(tmp_path, monkeypatch):
    monkeypatch.setattr("app.db.DB_PATH", tmp_path / "test.db")
    from app import seed

    seed.init_db()
    return tmp_path / "test.db"


def test_tile_default_cycle_used_when_request_omits(fresh_db):
    from app.services import estimate_service

    # seeded tile 2 (800x800) carries default pattern_cycle=2.0
    r = estimate_service.run_estimate(1, 2, None, False, "", None)
    assert r["pattern_cycle"] == 2.0
    assert r["pattern_extra"] == 6
    assert r["order_count"] == r["base_order_count"] + 6


def test_request_cycle_overrides_tile_default(fresh_db):
    from app.services import estimate_service

    off = estimate_service.run_estimate(1, 2, None, False, "", 0.0)
    assert off["pattern_extra"] == 0
    assert off["order_count"] == off["base_order_count"]

    on = estimate_service.run_estimate(1, 1, None, False, "", 2.0)
    assert on["pattern_cycle"] == 2.0
    assert on["pattern_extra"] == 16


def test_invalid_cycle_returns_422(fresh_db):
    from app.services import estimate_service

    with pytest.raises(HTTPException) as e:
        estimate_service.run_estimate(1, 1, None, False, "", 6.0)
    assert e.value.status_code == 422
    with pytest.raises(HTTPException) as e:
        estimate_service.run_estimate(1, 1, None, False, "", -0.5)
    assert e.value.status_code == 422


def test_saved_run_keeps_extra_after_default_change(fresh_db):
    from app.repositories import history
    from app.repositories import tiles as tile_repo
    from app.services import estimate_service

    saved = estimate_service.run_estimate(1, 2, None, True, "快照", None)
    assert saved["pattern_extra"] == 6

    # changing only the tile's default cycle must not rewrite stored runs
    tile_repo.update_pattern_cycle(2, 0.0)
    run = history.get_run(saved["run_id"])
    assert run["result"]["pattern_cycle"] == 2.0
    assert run["result"]["pattern_extra"] == 6
    assert run["result"]["order_count"] == saved["order_count"]

    # new estimates now follow the updated default
    fresh = estimate_service.run_estimate(1, 2, None, False, "", None)
    assert fresh["pattern_extra"] == 0
