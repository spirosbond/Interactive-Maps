from datetime import datetime, timezone
from fastapi import (
    HTTPException,
    status,
    APIRouter,
)

from app.models import iss
from app.db import SatellitesCRUD, LocationsCRUD
from app.utils.model_utils import objectid_to_str
from app.config import app_config
from app.utils.model_utils import objectid_to_str
from app.components.location import LocationComponent

router = APIRouter()


# Get the Timestamps when the ISS is exposed to the sun
@router.get(
    "/sun",
    response_model=iss.ISSSun,
    summary="Timestamps when the ISS is exposed to the sun",
)
def iss_sun():
    # Retrieve the iss satellite from the database
    iss = SatellitesCRUD.find_one({"sat_id": app_config.app_iss_id})
    if iss is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ISS Satellite with id {app_config.app_iss_id} not found in db.",
        )

    # Get all locations of the ISS sorted by ascending order
    pipeline = [
        {"$match": {"sat_id": iss["sat_id"]}},
        {"$sort": {"timestamp": 1}},  # 1 for ascending order (oldest to newest)
    ]
    try:
        locations = LocationsCRUD.aggregate(pipeline)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Error retrieving locations for {iss}: {e}",
        )

    # The windows List will store or time windows of "daylight"
    locationComponent = LocationComponent()
    try:
        windows = locationComponent.get_daylight_windows(locations)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating daylight windows for {iss}: {e}",
        )

    return {
        "sat_id": iss["sat_id"],
        "results": len(windows),
        "windows": windows,
    }


# Get the last known location of the iss. We are capturing the location of the ISS with the Background task at the maximum frequency (20s).
# So we consider the last known location as the "present time".
@router.get(
    "/position",
    response_model=iss.ISSPos,
    summary="Get the last known location of the iss",
)
def iss_loc():
    # Retrieve the iss satellite from the database
    iss = SatellitesCRUD.find_one({"sat_id": app_config.app_iss_id})
    if iss is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ISS Satellite with id {app_config.app_iss_id} not found in db.",
        )

    # Search the last location captured for the ISS.
    pipeline = [
        {"$match": {"sat_id": iss["sat_id"]}},
        {"$sort": {"timestamp": -1}},  # -1 for descending order (newest to oldest),
        {"$limit": 1},  # Setting limit to 1 optimizes performance for the search
    ]
    try:
        # Aggregate() returns a List
        locations = LocationsCRUD.aggregate(pipeline)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Error retrieving last location for {iss}: {e}",
        )
    # Prepare the return message
    return_dict = {
        "sat_id": iss["sat_id"],
    }
    # If there is an element in the list, update the return message
    if locations:
        return_dict["latitude"] = locations[0]["latitude"]
        return_dict["longitude"] = locations[0]["longitude"]
        return_dict["timestamp"] = locations[0]["timestamp"]
    return return_dict
