from fastapi import status, APIRouter, HTTPException

from app.models import location
from app.db import LocationsCRUD
from app.utils.model_utils import objectid_to_str

router = APIRouter()


@router.get(
    "/", response_model=location.ListLocationResponses, summary="Get the first records"
)
def get_locations(
    limit: int = 10,
    page: int = 1,
):
    # Calculate the right amount of skipped pages based on input
    skip = (page - 1) * limit
    pipeline = [
        {"$match": {}},
        {"$skip": skip},
        {"$limit": limit},
    ]

    # Run pipeline and get the locations
    try:
        locations = LocationsCRUD.aggregate(pipeline)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Error retrieving locations with pipeline {pipeline}: {e}",
        )
    return {
        "status": "success",
        "results": len(locations),
        "total": LocationsCRUD.count(),
        "locations": objectid_to_str(locations),
    }


@router.get(
    "/{locationId}",
    response_model=location.LocationResponse,
    summary="Get single location using Database ID",
)
def get_location(
    locationId: str,
):
    # Try to get the required location. The CRUD function is managing the HttpExceptions
    result = LocationsCRUD.read(locationId)

    return {"status": "success", "location": objectid_to_str(result)}


@router.get(
    "/by_sat_id/{sat_id}",
    response_model=location.ListLocationResponses,
    summary="Get the last records for a specific satellite (sat_id)",
)
def get_last_locations(
    sat_id: int,
    limit: int = 10,
    page: int = 1,
):
    # Calculate the right amount of skipped pages based on input
    skip = (page - 1) * limit
    pipeline = [
        {"$match": {"sat_id": sat_id}},
        {"$skip": skip},
        {"$sort": {"timestamp": -1}},  # -1 for descending order (newest to oldest),
        {"$limit": limit},
    ]

    # Run pipeline and get the locations
    try:
        locations = LocationsCRUD.aggregate(pipeline)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Error retrieving locations with pipeline {pipeline}: {e}",
        )
    # Raise an exception if no locations were found
    if not locations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No locations found for sat_id {sat_id}.",
        )
    return {
        "status": "success",
        "results": len(locations),
        "total": len(locations),
        "locations": objectid_to_str(locations),
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
    # Create a new Location ignoring all None properties. The CRUD function is managing the HttpExceptions
    result = LocationsCRUD.create(payload.dict(exclude_none=True))

    # Try to read the newly created location to confirm it was created. The CRUD function is managing the HttpExceptions
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
    # Deletes a location based on an ID. The CRUD function is managing the HttpExceptions
    success, result = LocationsCRUD.delete(locationId)

    return {"status": "success", "location": objectid_to_str(result)}
