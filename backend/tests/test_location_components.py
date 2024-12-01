import pytest
from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime, timezone

# Required row to be able to import the app folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.components.location import LocationComponent

client = TestClient(app)

# Location 1
test_location_1 = {
    "visibility": "daylight",
    "timestamp": datetime(2024, 12, 1, 0, 0, 0, 0, tzinfo=timezone.utc).timestamp(),
}

# Location 2 with timestamp 30seconds after Location 1
test_location_2 = {
    "visibility": "eclipsed",
    "timestamp": test_location_1["timestamp"] + 30,
}

# Location 3 with timestamp 30seconds after Location 2
test_location_3 = {
    "visibility": "daylight",
    "timestamp": test_location_2["timestamp"] + 30,
}

# Location 4 with timestamp 30seconds after Location 3
test_location_4 = {
    "visibility": "eclipsed",
    "timestamp": test_location_3["timestamp"] + 30,
}


def test01_get_daylight_windows():
    locationComponent = LocationComponent()

    # Expect 2 windows with all locations in sequence
    windows = locationComponent.get_daylight_windows(
        [test_location_1, test_location_2, test_location_3, test_location_4]
    )
    print(windows)
    assert len(windows) == 2

    # Expect 1 window with only the 1st location and until last location
    windows = locationComponent.get_daylight_windows([test_location_1, test_location_4])
    print(windows)
    assert len(windows) == 1

    # Expect 1 window with only the 1st location and until location 3
    windows = locationComponent.get_daylight_windows([test_location_1, test_location_3])
    print(windows)
    assert len(windows) == 1

    # Expect 0 window with only eclipsed locations
    windows = locationComponent.get_daylight_windows([test_location_2, test_location_4])
    print(windows)
    assert len(windows) == 0

    # Expect 1 window with the same start and end
    windows = locationComponent.get_daylight_windows([test_location_1])
    print(windows)
    assert len(windows) == 1

    # Test all exceptions of function
    with pytest.raises(KeyError):
        test_location_1.pop("visibility")
        windows = locationComponent.get_daylight_windows([test_location_1])

    with pytest.raises(TypeError):
        test_location_3["timestamp"] = "2024-01-01T00:00:00"
        windows = locationComponent.get_daylight_windows([test_location_3])

    with pytest.raises(ValueError):
        test_location_3["timestamp"] = 999999999999
        windows = locationComponent.get_daylight_windows([test_location_3])

    with pytest.raises(OverflowError):
        test_location_3["timestamp"] = 999999999999999999999999
        windows = locationComponent.get_daylight_windows([test_location_3])
