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
    "visibility": "test visibility",
    "footprint": 5,
    "timestamp": "1900-01-01T00:00:00",
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
    "visibility": "test visibility",
    "footprint": 15,
    "timestamp": "1900-01-01T00:00:00",
    "daynum": 16,
    "solar_lat": 17,
    "solar_lon": 18,
    "units": "test unit",
}


def test01_get_locations():
    response = client.get("/api/location/?limit=10&page=1&search=")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["results"] >= 0
    assert isinstance(data["locations"], list)


def test02_create_location():
    # Try to create a location whithout the satellite existin. This should fail
    response = client.post("/api/location/", json=test_location_1)
    assert response.status_code == 400

    # Create a satellite first to link the location to
    response = client.post("/api/satellite/", json=test_satellite)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    satellite = data["satellite"]
    assert isinstance(satellite["_id"], str)
    test_satellite["_id"] = satellite["_id"]
    assert satellite == test_satellite

    response = client.post("/api/location/", json=test_location_1)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    location = data["location"]
    assert isinstance(location["_id"], str)
    test_location_1["_id"] = location["_id"]
    assert location == test_location_1

    response = client.post("/api/location/", json=test_location_2)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    location = data["location"]
    assert isinstance(location["_id"], str)
    test_location_2["_id"] = location["_id"]
    assert location == test_location_2


def test03_get_location_after_creation():
    location_id = test_location_1["_id"]
    response = client.get(f"/api/location/{location_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["location"] == test_location_1

    location_id = test_location_2["_id"]
    response = client.get(f"/api/location/{location_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["location"] == test_location_2


def test04_get_locations_by_sat_id():
    satellite_sat_id = test_satellite["sat_id"]
    assert satellite_sat_id is not None
    response = client.get(f"/api/location/by_sat_id/{satellite_sat_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["results"] == 2
    assert isinstance(data["locations"], list)
    assert len(data["locations"]) == 2


def test05_delete_location_no_cascade():
    location_id = test_location_1["_id"]
    assert location_id is not None

    # Delete the location
    delete_response = client.delete(f"/api/location/{location_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "success"
    assert delete_data["location"]["sat_id"] == test_location_1["sat_id"]


def test06_delete_location_with_cascade():
    satellite_id = test_satellite["_id"]
    assert satellite_id is not None

    # Delete the satellite
    delete_response = client.delete(f"/api/satellite/{satellite_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "success"
    assert delete_data["satellite"]["sat_id"] == test_satellite["sat_id"]


def test07_get_satellite_after_deletion():
    location_id = test_location_1["_id"]
    response = client.get(f"/api/satellite/{location_id}")
    assert response.status_code == 404

    location_id = test_location_2["_id"]
    response = client.get(f"/api/satellite/{location_id}")
    assert response.status_code == 404
