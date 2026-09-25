from pydantic import BaseModel, Field


class EstimateRequest(BaseModel):
    room_id: int
    tile_id: int
    waste_pct: float | None = None
    # per-run 花铺循环长 (m); null falls back to the tile's default; 0 disables
    pattern_cycle: float | None = Field(default=None, ge=0)
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
    pattern_extra: int
    pattern: dict
    order_count: int
    layout: dict
    run_id: int | None = None
