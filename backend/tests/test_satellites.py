import pytest
from fastapi.testclient import TestClient
import sys
import os

# Required row to be able to import the app folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.models.satellite import SatelliteSchema

client = TestClient(app)

# Shared test data
test_satellite = {
    "sat_id": 99999,
    "name": "Test Satellite",
    "units": "kilometers",
}


def test01_get_satellites():
    response = client.get("/api/satellite/?limit=10&page=1&search=")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["results"] >= 0
    assert isinstance(data["satellites"], list)


def test02_create_satellite():
    response = client.post("/api/satellite/", json=test_satellite)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    satellite = data["satellite"]
    assert isinstance(satellite["_id"], str)
    test_satellite["_id"] = satellite["_id"]
    assert satellite == test_satellite


def test03_get_satellite_after_creation():
    satellite_id = test_satellite["_id"]
    response = client.get(f"/api/satellite/{satellite_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["satellite"] == test_satellite


def test04_delete_satellite():
    satellite_id = test_satellite["_id"]
    assert satellite_id is not None

    # Delete the satellite
    delete_response = client.delete(f"/api/satellite/{satellite_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "success"
    assert delete_data["satellite"]["sat_id"] == test_satellite["sat_id"]


def test05_get_satellite_after_deletion():
    satellite_id = test_satellite["_id"]
    response = client.get(f"/api/satellite/{satellite_id}")
    assert response.status_code == 404
