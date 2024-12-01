import time
from typing import Dict, Tuple
from app.db import SatellitesCRUD, LocationsCRUD
import requests
from app.config import app_config


def main() -> Tuple[Dict, int]:
    """
    Function that pulls the iss location from the provided API. This is built in
    a way to be compatible with background tasks, services or cloud functions.
    Look at app_config.yaml for how it is defined and configured

    :returns:   Location that was pulled
    :rtype:     dict
    :returns:   The http status code of the request
    :rtype:     int
    """
    # Retrieve the iss satellite from the database
    iss = SatellitesCRUD.find_one({"sat_id": app_config.app_iss_id})

    if iss is None:
        print("ISS Satellite not found. Skipping...")
        return {}, 0
    # Define the API URL
    url = f"{app_config.app_apis_sat_loc_url}{iss['sat_id']}?units={iss['units']}"

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the JSON response to a Python dictionary
        loc = response.json()
        print("API Response as Dictionary:")
        print(loc)
        loc.pop("name")  # Remove name since it is not needed for the Location Schema
        loc["sat_id"] = loc.pop(
            "id"
        )  # Rename key "id" to "sat_id" to compy with the Location Schema

        # Store the new Location
        location = LocationsCRUD.create(loc)
        return location, response.status_code
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return {}, response.status_code
