from pydantic import BaseModel, Field


class TileUpdate(BaseModel):
    pattern_cycle: float = Field(ge=0)
