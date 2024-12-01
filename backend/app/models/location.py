from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class LocationSchema(BaseModel):
    sat_id: int
    latitude: float
    longitude: float
    altitude: float
    velocity: float
    visibility: str
    footprint: float
    timestamp: datetime
    daynum: float
    solar_lat: float
    solar_lon: float
    units: str


class LocationInDBSchema(LocationSchema):
    id: str = Field(None, alias="_id")


class LocationResponse(BaseModel):
    status: str
    location: LocationInDBSchema


class ListLocationResponses(BaseModel):
    status: str
    results: int
    total: int
    locations: List[LocationInDBSchema]
