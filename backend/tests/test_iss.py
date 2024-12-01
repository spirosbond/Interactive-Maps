import pytest
from fastapi.testclient import TestClient
import sys
import os

# Required row to be able to import the app folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.models.satellite import SatelliteSchema
from app.config import app_config

client = TestClient(app)


# Test case for the /sun endpoint to ensure it returns expected data structure and status code
def test01_iss_sun():
    # Make a GET request to the /sun endpoint
    response = client.get("/api/iss/sun")
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Parse the response JSON
    data = response.json()
    # Assert that the returned satellite ID matches the ISS ID configured in the app
    assert data["sat_id"] == app_config.app_iss_id
    # Assert that the 'results' field is a non-negative integer
    assert data["results"] >= 0
    # Assert that the 'windows' field is a list
    assert isinstance(data["windows"], list)
    # Assert that the 'windows' list has zero or more entries
    assert len(data["windows"]) >= 0


# Test case for the /position endpoint to ensure it returns expected data structure and status code
def test02_iss_loc():
    # Make a GET request to the /position endpoint
    response = client.get("/api/iss/position")
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Parse the response JSON
    data = response.json()
    # Assert that the returned satellite ID matches the ISS ID configured in the app
    assert data["sat_id"] == app_config.app_iss_id
    # Assert that the 'latitude' field is a float
    assert isinstance(data["latitude"], float)
    # Assert that the 'longitude' field is a float
    assert isinstance(data["longitude"], float)
    # Assert that the 'timestamp' field is a string (representing an ISO8601 timestamp)
    assert isinstance(data["timestamp"], str)
