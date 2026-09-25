import pytest

from app.engines.tile_math import tile_count


def test_pattern_cycle_zero_keeps_base_order():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, 0.0)
    assert r["base_order_count"] == 81
    assert r["pattern_extra"] == 0
    assert r["pattern_cycle"] == 0.0
    assert r["pattern"] == {"cycles": 0, "rows": 8}
    assert r["order_count"] == 81


def test_pattern_cycle_adds_cycles_times_rows():
    # cycles = ceil(6.0 / 1.2) = 5; rows = ceil(4.5 / 0.6) = 8; extra = 40
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, 1.2)
    assert r["pattern"]["cycles"] == 5
    assert r["pattern"]["rows"] == 8
    assert r["pattern_extra"] == 40
    assert r["base_order_count"] == 81
    assert r["order_count"] == 121


def test_pattern_cycle_uses_width_tile_rows():
    # corridor 8.0 x 1.2, 0.8 tile, cycle 2.0: cycles = 4, rows = ceil(1.2/0.8) = 2
    r = tile_count(8.0, 1.2, 0.8, 0.8, 0.0, 2.0)
    assert r["pattern"]["cycles"] == 4
    assert r["pattern"]["rows"] == 2
    assert r["pattern_extra"] == 8
    assert r["order_count"] == r["base_order_count"] + 8


def test_pattern_cycle_negative_fails():
    with pytest.raises(ValueError):
        tile_count(6.0, 4.5, 0.6, 0.6, 8.0, -1.0)


def test_pattern_cycle_ge_room_length_fails():
    with pytest.raises(ValueError):
        tile_count(6.0, 4.5, 0.6, 0.6, 8.0, 6.0)
    with pytest.raises(ValueError):
        tile_count(6.0, 4.5, 0.6, 0.6, 8.0, 7.0)
