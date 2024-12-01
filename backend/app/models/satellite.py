from pydantic import BaseModel, Field
from typing import List

"""
Schema that holds the Satellite information.
This is almost identical to the https://api.wheretheiss.at/v1/satellites/ schema for easy ingestion
"""


class SatelliteSchema(BaseModel):
    sat_id: int = Field(..., description="Unique satellite identifier")
    name: str
    units: str = "kilometers"


"""
SatelliteSchema with the addition of the "_id" that MongoDB will assign
"""


class SatelliteInDBSchema(SatelliteSchema):
    id: str = Field(None, alias="_id")


"""
Schema used whenever there is a need to reply with a SatelliteSchema
"""


class SatelliteResponse(BaseModel):
    status: str
    satellite: SatelliteInDBSchema


"""
Schema used whenever there is a need to reply with a list of SatelliteSchemas
"""


class ListSatelliteResponses(BaseModel):
    status: str
    results: int
    total: int
    satellites: List[SatelliteInDBSchema]
