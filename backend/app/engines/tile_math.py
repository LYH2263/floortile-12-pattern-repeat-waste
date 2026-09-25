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
    pattern_extra: pattern-match extras when tiling along the room's long side.
        cycles = ceil(room_l / pattern_cycle), rows = ceil(room_w / tile_w),
        extra = cycles * rows; order_count = base_order_count + extra.
        pattern_cycle == 0 disables it (extra = 0).
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    base_order = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    layout = layout_preview(room_l, room_w, tile_l, tile_w)

    cycle = float(pattern_cycle)
    cycles = 0
    extra = 0
    if cycle != 0.0:
        if cycle < 0:
            raise ValueError("pattern_cycle must be >= 0 (0 disables)")
        if cycle >= float(room_l):
            raise ValueError("pattern_cycle must be shorter than room length")
        cycles = ceil_units(float(room_l) / cycle)
        # one extra matching piece per cycle per row laid across the room width
        extra = cycles * layout["rows"]

    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "base_order_count": base_order,
        "pattern_extra": extra,
        "pattern_cycle": cycle,
        "pattern": {"cycles": cycles, "rows": layout["rows"]},
        "order_count": base_order + extra,
        "layout": layout,
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
