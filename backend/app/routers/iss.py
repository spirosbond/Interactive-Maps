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
        # {"$match": {"sat_id": iss["sat_id"], "visibility": "daylight"}},
        {"$match": {"sat_id": iss["sat_id"]}},
        {"$sort": {"timestamp": 1}},  # 1 for ascending order (oldest to newest)
    ]
    locations = LocationsCRUD.aggregate(pipeline)

    # Prepare the return message with no daylight windows
    return_dict = {
        "sat_id": iss["sat_id"],
        "results": 0,
        "windows": [],
    }

    # The windows List will store or time windows of "daylight"
    windows = []

    # If any locations found
    if locations:
        # The window dictionary will store one daylight window with it's start and end time
        window = {}
        # Go through all locations
        for location in locations:
            # If it is daylight and the window start is undefined (new window) save it
            if location["visibility"] == "daylight" and window.get("start") is None:
                window["start"] = datetime.fromtimestamp(
                    location["timestamp"], tz=timezone.utc
                )
            # Else if it is eclipsed and there is alread a window open, then close the window with the timestamp of the eclipse
            elif (
                location["visibility"] == "eclipsed" and window.get("start") is not None
            ):
                window["end"] = datetime.fromtimestamp(
                    location["timestamp"], tz=timezone.utc
                )
                # Add the closed window to the list and reset it
                windows.append(window.copy())
                window = {}
        # If there is still an open window after going through all locations (last location still in daylight), then close it with the last known timestamp
        if window.get("start") is not None:
            window["end"] = datetime.fromtimestamp(
                locations[-1]["timestamp"], tz=timezone.utc
            )
            windows.append(window.copy())
            window = {}

        # Update the return message with the found windows their number. If none found, windows List will be empty
        return_dict["windows"] = windows
        return_dict["results"] = len(windows)
    return return_dict


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
    # Aggregate() returns a List
    locations = LocationsCRUD.aggregate(pipeline)

    # Prepare the return message with no daylight windows
    return_dict = {
        "sat_id": iss["sat_id"],
    }
    # If there is an element in the list,update the return message
    if locations:
        return_dict["latitude"] = locations[0]["latitude"]
        return_dict["longitude"] = locations[0]["longitude"]
        return_dict["timestamp"] = locations[0]["timestamp"]
    return return_dict
