from fastapi import (
    status,
    APIRouter,
)

from app.models import location
from app.db import LocationsCRUD
from app.utils.model_utils import objectid_to_str

router = APIRouter()


# Get First 10 Records
@router.get(
    "/", response_model=location.ListLocationResponses, summary="Get the first records"
)
def get_locations(
    limit: int = 10,
    page: int = 1,
):
    skip = (page - 1) * limit
    pipeline = [
        {"$match": {}},
        {"$skip": skip},
        {"$limit": limit},
    ]
    locations = LocationsCRUD.aggregate(pipeline)

    return {
        "status": "success",
        "results": len(locations),
        "total": LocationsCRUD.count(),
        "locations": objectid_to_str(locations),
    }


@router.get(
    "/{locationId}",
    response_model=location.LocationResponse,
    summary="Get location using Database ID",
)
def get_location(
    locationId: str,
):
    result = LocationsCRUD.read(locationId)
    # new_satellite = SatellitesCRUD.read(str(result["_id"]))

    return {"status": "success", "location": objectid_to_str(result)}


# Get Last 10 Records
@router.get(
    "/by_sat_id/{sat_id}",
    response_model=location.ListLocationResponses,
    summary="Get the last records for a specific satellite",
)
def get_last_locations(
    sat_id: int,
    limit: int = 10,
    page: int = 1,
):
    skip = (page - 1) * limit
    pipeline = [
        {"$match": {"sat_id": sat_id}},
        {"$skip": skip},
        {"$sort": {"timestamp": -1}},  # -1 for descending order (newest to oldest),
        # {"$limit": limit},
    ]
    locations = LocationsCRUD.aggregate(pipeline)
    ret_locations = locations[0:limit]
    return {
        "status": "success",
        "results": len(ret_locations),
        "total": len(locations),
        "locations": objectid_to_str(ret_locations),
    }


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=location.LocationResponse,
    summary="Create a new record",
)
def create_location(
    payload: location.LocationSchema,
):
    result = LocationsCRUD.create(payload.dict(exclude_none=True))
    new_location = LocationsCRUD.read(str(result["_id"]))

    return {"status": "success", "location": objectid_to_str(new_location)}


@router.delete(
    "/{locationId}",
    response_model=location.LocationResponse,
    summary="Delete a record",
)
def delete_satellite(
    locationId: str,
):
    success, result = LocationsCRUD.delete(locationId)

    return {"status": "success", "location": objectid_to_str(result)}
