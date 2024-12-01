from fastapi import (
    status,
    APIRouter,
)

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
    skip = (page - 1) * limit
    pipeline = [
        {
            "$match": {
                "name": {"$regex": search, "$options": "i"},
                # "user_id": str(current_user["_id"])
            }
        },
        {"$skip": skip},
        {"$limit": limit},
    ]
    satellites = SatellitesCRUD.aggregate(pipeline)

    return {
        "status": "success",
        "results": len(satellites),
        "total": SatellitesCRUD.count(),
        "satellites": objectid_to_str(satellites),
    }


@router.get(
    "/{satelliteId}",
    response_model=satellite.SatelliteResponse,
    summary="Get satellite using Database ID",
)
def get_satellite(
    satelliteId: str,
):
    result = SatellitesCRUD.read(satelliteId)
    # new_satellite = SatellitesCRUD.read(str(result["_id"]))

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
    result = SatellitesCRUD.create(payload.dict(exclude_none=True))
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
    success, result = SatellitesCRUD.delete(satelliteId)

    return {"status": "success", "satellite": objectid_to_str(result)}
