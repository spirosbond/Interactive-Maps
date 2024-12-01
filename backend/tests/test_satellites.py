import pytest
from fastapi.testclient import TestClient
import sys
import os

# Required row to be able to import the app folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.models.satellite import SatelliteSchema

# Create a TestClient instance for testing the FastAPI app
client = TestClient(app)

# Shared test data for creating a satellite
test_satellite = {
    "sat_id": 99999,
    "name": "Test Satellite",
    "units": "kilometers",
}


# Test for fetching the first 10 satellites (GET /api/satellite/)
def test01_get_satellites():
    # Send GET request to retrieve the first 10 satellites
    response = client.get("/api/satellite/?limit=10&page=1&search=")
    assert response.status_code == 200  # Ensure the response status code is 200 (OK)
    data = response.json()
    assert data["status"] == "success"  # Verify the status in the response
    assert data["results"] >= 0  # Ensure results count is non-negative
    assert isinstance(data["satellites"], list)  # Verify satellites field is a list


# Test for creating a new satellite (POST /api/satellite/)
def test02_create_satellite():
    # Send POST request to create a new satellite
    response = client.post("/api/satellite/", json=test_satellite)
    assert (
        response.status_code == 201
    )  # Ensure the response status code is 201 (Created)
    data = response.json()
    assert data["status"] == "success"  # Verify the status in the response
    satellite = data["satellite"]
    assert isinstance(satellite["_id"], str)  # Ensure the satellite ID is a string
    test_satellite["_id"] = satellite[
        "_id"
    ]  # Save the created satellite ID for later tests
    assert (
        satellite == test_satellite
    )  # Verify the created satellite matches the input data


# Test for retrieving the created satellite (GET /api/satellite/{satelliteId})
def test03_get_satellite_after_creation():
    satellite_id = test_satellite["_id"]  # Use the ID of the created satellite
    # Send GET request to retrieve the satellite by ID
    response = client.get(f"/api/satellite/{satellite_id}")
    assert response.status_code == 200  # Ensure the response status code is 200 (OK)
    data = response.json()
    assert data["status"] == "success"  # Verify the status in the response
    assert (
        data["satellite"] == test_satellite
    )  # Ensure the retrieved satellite matches the created one


# Test for deleting the created satellite (DELETE /api/satellite/{satelliteId})
def test04_delete_satellite():
    satellite_id = test_satellite["_id"]  # Use the ID of the created satellite
    assert satellite_id is not None  # Ensure the satellite ID is not None

    # Send DELETE request to remove the satellite
    delete_response = client.delete(f"/api/satellite/{satellite_id}")
    assert (
        delete_response.status_code == 200
    )  # Ensure the response status code is 200 (OK)
    delete_data = delete_response.json()
    assert delete_data["status"] == "success"  # Verify the status in the response
    assert (
        delete_data["satellite"]["sat_id"] == test_satellite["sat_id"]
    )  # Verify the deleted satellite matches


# Test for retrieving the deleted satellite (GET /api/satellite/{satelliteId})
def test05_get_satellite_after_deletion():
    satellite_id = test_satellite["_id"]  # Use the ID of the deleted satellite
    # Send GET request to retrieve the satellite by ID
    response = client.get(f"/api/satellite/{satellite_id}")
    assert (
        response.status_code == 404
    )  # Ensure the response status code is 404 (Not Found)
