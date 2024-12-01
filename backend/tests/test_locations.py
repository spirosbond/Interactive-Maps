import pytest
from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime

# Required row to be able to import the app folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.models.location import LocationSchema

client = TestClient(app)

# Shared test data
test_satellite = {
    "sat_id": 99999,
    "name": "Test Satellite",
    "units": "kilometers",
}

# Location 1 will be used to test the Location "delete" endpoint without cascading effect
test_location_1 = {
    "sat_id": test_satellite["sat_id"],
    "latitude": 1,
    "longitude": 2,
    "altitude": 3,
    "velocity": 4,
    "visibility": "daylight",
    "footprint": 5,
    "timestamp": "2024-01-01T00:00:00",
    "daynum": 6,
    "solar_lat": 7,
    "solar_lon": 8,
    "units": "test unit",
}

# Location 2 will be used to test the Satellite "delete" endpoint with cascading effect
test_location_2 = {
    "sat_id": test_satellite["sat_id"],
    "latitude": 11,
    "longitude": 12,
    "altitude": 13,
    "velocity": 14,
    "visibility": "eclipsed",
    "footprint": 15,
    "timestamp": "2024-01-01T02:00:00",
    "daynum": 16,
    "solar_lat": 17,
    "solar_lon": 18,
    "units": "test unit",
}


def test01_get_locations():
    # Test the endpoint to retrieve a list of locations.
    response = client.get("/api/location/?limit=10&page=1&search=")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["results"] >= 0  # Check that the results count is non-negative.
    assert isinstance(
        data["locations"], list
    )  # Ensure the locations are returned as a list.


def test02_create_location():
    # Test creating a location without an existing satellite. This should fail.
    response = client.post("/api/location/", json=test_location_1)
    assert response.status_code == 400

    # Create a satellite to associate with the location.
    response = client.post("/api/satellite/", json=test_satellite)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    satellite = data["satellite"]
    assert isinstance(satellite["_id"], str)  # Verify that the satellite has an ID.
    test_satellite["_id"] = satellite["_id"]
    assert (
        satellite == test_satellite
    )  # Confirm the created satellite matches the input data.

    # Create the first location linked to the satellite.
    response = client.post("/api/location/", json=test_location_1)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    location = data["location"]
    assert isinstance(location["_id"], str)  # Verify that the location has an ID.
    test_location_1["_id"] = location["_id"]
    assert (
        location == test_location_1
    )  # Confirm the created location matches the input data.

    # Create the second location linked to the satellite.
    response = client.post("/api/location/", json=test_location_2)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    location = data["location"]
    assert isinstance(location["_id"], str)  # Verify that the location has an ID.
    test_location_2["_id"] = location["_id"]
    assert (
        location == test_location_2
    )  # Confirm the created location matches the input data.


def test03_get_location_after_creation():
    # Test retrieving the first created location by its ID.
    location_id = test_location_1["_id"]
    response = client.get(f"/api/location/{location_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert (
        data["location"] == test_location_1
    )  # Verify the retrieved location matches the input data.

    # Test retrieving the second created location by its ID.
    location_id = test_location_2["_id"]
    response = client.get(f"/api/location/{location_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert (
        data["location"] == test_location_2
    )  # Verify the retrieved location matches the input data.


def test04_get_locations_by_sat_id():
    # Test retrieving locations by the satellite's `sat_id`.
    satellite_sat_id = test_satellite["sat_id"]
    assert satellite_sat_id is not None
    response = client.get(f"/api/location/by_sat_id/{satellite_sat_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["results"] == 2  # Ensure two locations are returned for the satellite.
    assert isinstance(
        data["locations"], list
    )  # Verify the locations are returned as a list.
    assert (
        len(data["locations"]) == 2
    )  # Confirm the number of locations matches the expected count.


def test05_delete_location_no_cascade():
    # Test deleting a location without cascading effects.
    location_id = test_location_1["_id"]
    assert location_id is not None

    # Send a delete request for the location.
    delete_response = client.delete(f"/api/location/{location_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "success"
    assert (
        delete_data["location"]["sat_id"] == test_location_1["sat_id"]
    )  # Verify the correct location was deleted.


def test06_delete_location_with_cascade():
    # Test deleting a satellite and cascading deletion of associated locations.
    satellite_id = test_satellite["_id"]
    assert satellite_id is not None

    # Send a delete request for the satellite.
    delete_response = client.delete(f"/api/satellite/{satellite_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "success"
    assert (
        delete_data["satellite"]["sat_id"] == test_satellite["sat_id"]
    )  # Verify the correct satellite was deleted.


def test07_get_satellite_after_deletion():
    # Test retrieving locations by satellite ID after it has been deleted.
    location_id = test_location_1["_id"]
    response = client.get(f"/api/satellite/{location_id}")
    assert response.status_code == 404  # Confirm the satellite no longer exists.

    location_id = test_location_2["_id"]
    response = client.get(f"/api/satellite/{location_id}")
    assert response.status_code == 404  # Confirm the satellite no longer exists.
