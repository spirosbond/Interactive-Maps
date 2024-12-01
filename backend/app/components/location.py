from typing import Any, List, Dict
from app.models.location import LocationInDBSchema
from datetime import datetime, timezone


class LocationComponent:
    """
    This class implements components related to Locations
    """

    def __init__(self):
        pass

    def get_daylight_windows(self, locations: List[Dict]) -> List[Dict]:
        """
        Finds the the daylight windows froma  list of locations.

        :param      locations:      The list of locations
        :type       locations:      Dictionary compliant with LocationSchema

        :returns:   The daylight windows.
        :rtype:     List[Dict] with the keys "start" and "end"
        """
        windows = []

        if locations:
            window = {}
            for location in locations:
                try:
                    # If it is daylight and the window start is undefined (new window) save it
                    if (
                        location["visibility"] == "daylight"
                        and window.get("start") is None
                    ):
                        window["start"] = datetime.fromtimestamp(
                            location["timestamp"], tz=timezone.utc
                        )
                        # window["start"] = location["timestamp"]
                    # Else if it is eclipsed and there is already a window open, then close the window
                    elif (
                        location["visibility"] == "eclipsed"
                        and window.get("start") is not None
                    ):
                        window["end"] = datetime.fromtimestamp(
                            location["timestamp"], tz=timezone.utc
                        )
                        # window["end"] = location["timestamp"]
                        windows.append(window.copy())
                        window = {}
                except KeyError as e:
                    raise KeyError(
                        f"Error related to missing or invalid keys while processing location: {location}: {e}"
                    )
                except TypeError as e:
                    raise TypeError(
                        f"Error related to missing or invalid keys while processing location: {location}: {e}"
                    )
                except ValueError as e:
                    raise ValueError(
                        f"Error related to invalid or out-of-range timestamps while processing location: {location}: {e}"
                    )

                except OverflowError as e:
                    raise OverflowError(
                        f"Error related to invalid or out-of-range timestamps while processing location: {location}: {e}"
                    )

            # If there is still an open window after going through all locations
            if window.get("start") is not None:
                window["end"] = datetime.fromtimestamp(
                    locations[-1]["timestamp"], tz=timezone.utc
                )
                # window["end"] = locations[-1]["timestamp"]
                windows.append(window.copy())

        return windows
