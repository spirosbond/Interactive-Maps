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


def test01_iss_sun():
    response = client.get("/api/iss/sun")
    assert response.status_code == 200
    data = response.json()
    assert data["sat_id"] == app_config.app_iss_id
    assert data["results"] >= 0
    assert isinstance(data["windows"], list)
    assert len(data["windows"]) >= 0


def test02_iss_loc():
    response = client.get("/api/iss/position")
    assert response.status_code == 200
    data = response.json()
    assert data["sat_id"] == app_config.app_iss_id
    assert isinstance(data["latitude"], float)
    assert isinstance(data["longitude"], float)
    assert isinstance(data["timestamp"], str)
