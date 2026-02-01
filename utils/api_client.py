import requests
import logging
from typing import Dict, Optional


class OpenMeteoAPIClient:
    """API client for Open-Meteo"""

    def __init__(self, base_url: str):
        self.base_url = base_url

        self.session = requests.Session()

        self.logger = logging.getLogger(__name__)

    def get(self, endpoint: str, params: Optional[Dict] = None):
        """
        Perform GET request

        Args:
            endpoint: API endpoint (e.g., "/forecast")
            params: Query parameters (e.g., {"latitude": 52.52, "longitude": 13.41})

        Returns:
            Response object
        """

        url = self.base_url + endpoint

        self.logger.info(f"GET request to: {url}")

        response = self.session.get(url, params=params, timeout=5)
        self.logger.info(f"Response status: {response.status_code}")

        return response

    def close(self):
        """Close the session"""
        self.session.close()


class OpenMeteoResponseValidator:
    """Validator for API responses"""

    @staticmethod
    def validate_status_code(response, expected_status: int):
        """Validate response status code"""

        actual_status = response.status_code

        assert (
            actual_status == expected_status
        ), f"Expected status {expected_status}, got {actual_status}"

    @staticmethod
    def validate_json_response(response):
        """Validate response is valid JSON"""
        try:

            data = response.json()
            assert data is not None
            return True
        except ValueError:
            raise AssertionError("Response is not valid JSON")

    @staticmethod
    def validate_response_time(response, max_time: float = 3.0):
        """Validate response time is acceptable"""
        response_time = response.elapsed.total_seconds()
        assert (
            response_time <= max_time
        ), f"Response time exceeded {max_time}s. Actual: {response_time:.2f}s"
