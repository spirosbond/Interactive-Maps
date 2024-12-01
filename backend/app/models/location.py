from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

"""
Schema that holds the Location information from a satellite.
This is almost identical to the https://api.wheretheiss.at/v1/satellites/ schema for easy ingestion
"""


class LocationSchema(BaseModel):
    sat_id: int  # Used to link the location to a satellite
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


"""
LocationSchema with the addition of the "_id" that MongoDB will assign
"""


class LocationInDBSchema(LocationSchema):
    id: str = Field(None, alias="_id")


"""
Schema used whenever there is a need to reply with a LocationSchema
"""


class LocationResponse(BaseModel):
    status: str
    location: LocationInDBSchema


"""
Schema used whenever there is a need to reply with a list of LocationSchemas
"""


class ListLocationResponses(BaseModel):
    status: str
    results: int
    total: int
    locations: List[LocationInDBSchema]
