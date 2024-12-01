from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict
from app.models.location import LocationInDBSchema

"""
Schema that holds the information as requested in the assignment:
...expose a GET resource at /iss/sun that returns a list of time windows
during which the ISS was exposed to the sun, until present time.
"""


class ISSSun(BaseModel):
    sat_id: int
    results: int
    windows: List[Dict] | None = None


"""
Schema that holds the information as requested in the assignment:
...expose a GET resource at /iss/position that returns the latitude and
longitude of the ISS at present time

An alternative definition for the ISSPos Schema would be to utilize the the Location Schema (preferred).
I didn't go this way to comply with the instructions as much as possible. For example:

class ISSPos(BaseModel):
    status: str
    location: LocationInDBSchema
"""


class ISSPos(BaseModel):
    sat_id: int
    latitude: float | None = None
    longitude: float | None = None
    timestamp: datetime | None = None
