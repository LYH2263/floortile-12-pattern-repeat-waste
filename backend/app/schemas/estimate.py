from pydantic import BaseModel, Field


class EstimateRequest(BaseModel):
    room_id: int
    tile_id: int
    waste_pct: float | None = None
    pattern_cycle: float | None = None
    save: bool = False
    note: str = ""


class EstimateResponse(BaseModel):
    room_id: int
    tile_id: int
    room_name: str
    tile_name: str
    area_m2: float
    piece_m2: float
    raw_count: int
    waste_pct: float
    base_order_count: int
    pattern_cycle: float
    pattern_cycles: int
    pattern_extra: int
    order_count: int
    layout: dict
    run_id: int | None = None
