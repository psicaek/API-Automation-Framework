"""
Pytest fixtures
"""

import pytest
import logging
from utils.api_client import OpenMeteoAPIClient, OpenMeteoResponseValidator
from utils.config import OpenMeteoAPIConfig


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@pytest.fixture(scope="session")
def api_client():
    """Create API client"""
    # TODO: Create OpenMeteoAPIClient with BASE_URL from config
    client = OpenMeteoAPIClient(OpenMeteoAPIConfig.BASE_URL)
    yield client
    client.close()


@pytest.fixture(scope="session")
def validator():
    """Create response validator"""
    # TODO: Return OpenMeteoResponseValidator instance
    return OpenMeteoResponseValidator()


@pytest.fixture(scope="session")
def logger():
    """Provide logger"""
    return logging.getLogger("WeatherAPITests")
