from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.repositories import tiles as tile_repo

router = APIRouter(tags=["tiles"])


class TileUpdate(BaseModel):
    pattern_cycle: float = Field(..., ge=0)


@router.get("/tiles")
def list_tiles():
    return {"items": tile_repo.list_tiles()}


@router.get("/tiles/{tile_id}")
def get_tile(tile_id: int):
    row = tile_repo.get_tile(tile_id)
    if not row:
        raise HTTPException(404, "tile not found")
    return row


@router.put("/tiles/{tile_id}")
def update_tile(tile_id: int, body: TileUpdate):
    row = tile_repo.update_pattern_cycle(tile_id, body.pattern_cycle)
    if not row:
        raise HTTPException(404, "tile not found")
    return row
