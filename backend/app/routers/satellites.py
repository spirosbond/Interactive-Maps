from fastapi import status, APIRouter, HTTPException

from app.models import satellite
from app.db import SatellitesCRUD
from app.utils.model_utils import objectid_to_str

router = APIRouter()


# Get First 10 Records
@router.get(
    "/",
    response_model=satellite.ListSatelliteResponses,
    summary="Get the first records",
)
def get_satellites(
    limit: int = 10,
    page: int = 1,
    search: str = "",
):
    # Calculate the right amount of skipped pages based on input
    skip = (page - 1) * limit
    pipeline = [
        {
            "$match": {
                "name": {"$regex": search, "$options": "i"},
            }
        },
        {"$skip": skip},
        {"$limit": limit},
    ]

    # Run pipeline and get the satellites
    try:
        satellites = SatellitesCRUD.aggregate(pipeline)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Error retrieving locations with pipeline {pipeline}: {e}",
        )
    return {
        "status": "success",
        "results": len(satellites),
        "total": SatellitesCRUD.count(),
        "satellites": objectid_to_str(satellites),
    }


@router.get(
    "/{satelliteId}",
    response_model=satellite.SatelliteResponse,
    summary="Get single satellite using Database ID",
)
def get_satellite(
    satelliteId: str,
):
    # Try to get the required satelite. The CRUD function is managing the HttpExceptions
    result = SatellitesCRUD.read(satelliteId)

    return {"status": "success", "satellite": objectid_to_str(result)}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=satellite.SatelliteResponse,
    summary="Create a new record",
)
def create_satellite(
    payload: satellite.SatelliteSchema,
):
    # Create a new Satellite ignoring all None properties. The CRUD function is managing the HttpExceptions
    result = SatellitesCRUD.create(payload.dict(exclude_none=True))
    # Try to read the newly created satellite to confirm it was created. The CRUD function is managing the HttpExceptions
    new_satellite = SatellitesCRUD.read(str(result["_id"]))

    return {"status": "success", "satellite": objectid_to_str(new_satellite)}


@router.delete(
    "/{satelliteId}",
    response_model=satellite.SatelliteResponse,
    summary="Delete a record",
)
def delete_satellite(
    satelliteId: str,
):
    # Deletes a satellite based on an ID. The CRUD function is managing the HttpExceptions
    success, result = SatellitesCRUD.delete(satelliteId)

    return {"status": "success", "satellite": objectid_to_str(result)}
