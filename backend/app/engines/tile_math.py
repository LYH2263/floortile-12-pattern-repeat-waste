"""Floor tile order count: area method + optional grid layout preview."""

from app.engines.helpers import ceil_units


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    pattern_cycle: float = 0.0,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    base_order_count: ceil(raw * (1 + waste_pct/100))
    order_count: base_order_count + pattern_extra (pattern repeat matching along
    the room's long edge; pattern_cycle=0 disables it)
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    with_waste = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    pattern = pattern_repeat_extra(room_l, room_w, tile_l, tile_w, pattern_cycle)
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "base_order_count": with_waste,
        **pattern,
        "order_count": with_waste + pattern["pattern_extra"],
        "layout": layout,
    }


def pattern_repeat_extra(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    cycle: float,
) -> dict:
    """
    Extra tiles for pattern-repeat matching when laying along the room's long
    edge (room_l). Each of the ceil(room_l / cycle) repeat segments must start
    a fresh tile, so a row needs cycles * ceil(cycle / tile_l) tiles instead of
    ceil(room_l / tile_l); the difference times the row count is the extra.

    cycle == 0 disables matching (no extra). cycle < 0 or cycle >= room_l is
    rejected as a misconfiguration.
    """
    cycle = float(cycle)
    if cycle < 0:
        raise ValueError("pattern cycle must be >= 0")
    if cycle == 0:
        return {"pattern_cycle": 0.0, "pattern_cycles": 0, "pattern_extra": 0}
    if cycle >= float(room_l):
        raise ValueError("pattern cycle must be smaller than room length")
    cycles = ceil_units(float(room_l) / cycle)
    per_row = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    matched_per_row = cycles * ceil_units(cycle / float(tile_l))
    extra = max(0, matched_per_row - per_row) * rows
    return {
        "pattern_cycle": cycle,
        "pattern_cycles": cycles,
        "pattern_extra": extra,
    }


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method)."""
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }
