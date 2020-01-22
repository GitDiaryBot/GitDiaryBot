import logging

import requests


_LOCATION_FORMAT = "Latitude: {latitude}\nLongitude: {longitude}"
GEOCODING_API = (
    "https://maps.googleapis.com/maps/api/geocode/json"
)


logger = logging.getLogger(__name__)


class LocationTransformer:
    def __init__(self, google_api_key: str = None) -> None:
        self._google_api_key = google_api_key

    def handle_coordinates(self, latitude: float, longitude: float) -> str:
        latlon = _LOCATION_FORMAT.format(
            latitude=latitude,
            longitude=longitude,
        )
        if self._google_api_key:
            address = self._resolve_address(latitude, longitude)
            if address:
                message = f"{latlon}\nAddress: {address}"
            else:
                message = latlon
        else:
            message = latlon
        return message

    def _resolve_address(self, latitude: float, longitude: float) -> str:
        try:
            response = requests.get(
                GEOCODING_API,
                {
                    "latlng": f"{latitude},{longitude}",
                    "key": self._google_api_key,
                }
            )
            response.raise_for_status()
            data = response.json()
            error_message = data.get('error_message')
            if error_message:
                logger.error(error_message)
                return ""
            results = data.get('results')
            if results:
                return results[0]['formatted_address']
        except requests.RequestException:
            logger.exception("Failed to resolve address.")
        return ""
