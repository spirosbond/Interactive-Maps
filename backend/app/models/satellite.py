from pydantic import BaseModel, Field
from typing import List


class SatelliteSchema(BaseModel):
    sat_id: int = Field(..., description="Unique satellite identifier")
    name: str
    units: str = "kilometers"


class SatelliteInDBSchema(SatelliteSchema):
    id: str = Field(None, alias="_id")


class SatelliteResponse(BaseModel):
    status: str
    satellite: SatelliteInDBSchema


class ListSatelliteResponses(BaseModel):
    status: str
    results: int
    total: int
    satellites: List[SatelliteInDBSchema]
