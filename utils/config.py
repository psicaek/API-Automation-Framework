"""
Configuration for Open-Meteo API testing framework
"""


class OpenMeteoAPIConfig:
    """Open-Meteo API Configuration"""

    # Base URL
    BASE_URL = "https://api.open-meteo.com/v1"

    # Endpoints
    FORECAST_ENDPOINT = "/forecast"

    # Expected Response Times (in seconds)
    MAX_RESPONSE_TIME = 3.0

    # HTTP Status Codes
    STATUS_OK = 200
    STATUS_BAD_REQUEST = 400

    # Test Locations (Nuremberg coordinates)
    NUREMBERG_LAT = 49.4521
    NUREMBERG_LON = 11.0767
    NUREMBERG_CITY = "Nürnberg"
    BERLIN_LAT = 52.5200
    BERLIN_LON = 13.4050
    BERLIN_CITY = "Berlin"
    PATRAS_LAT = 38.2466
    PATRAS_LON = 21.7346
    PATRAS_CITY = "Patras"


class ValidationMessages:
    """Validation messages for assertions"""

    RESPONSE_TIME_EXCEEDED = "Response time exceeded {expected}s. Actual: {actual:.2f}s"
    STATUS_CODE_MISMATCH = "Expected status {expected}, got {actual}"
    INVALID_JSON = "Response is not valid JSON"
