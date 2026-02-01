import pytest
from utils.config import OpenMeteoAPIConfig


class TestCurrentWeather:
    """Test current weather endpoint"""

    @pytest.mark.parametrize(
        "latitude,longitude,city_name",
        [
            (
                OpenMeteoAPIConfig.NUREMBERG_LAT,
                OpenMeteoAPIConfig.NUREMBERG_LON,
                OpenMeteoAPIConfig.NUREMBERG_CITY,
            ),
            (
                OpenMeteoAPIConfig.PATRAS_LAT,
                OpenMeteoAPIConfig.PATRAS_LON,
                OpenMeteoAPIConfig.PATRAS_CITY,
            ),
            (
                OpenMeteoAPIConfig.BERLIN_LAT,
                OpenMeteoAPIConfig.BERLIN_LON,
                OpenMeteoAPIConfig.BERLIN_CITY,
            ),
        ],
    )
    def test_get_current_weather_multiple_cities(
        self, api_client, validator, logger, latitude, longitude, city_name
    ):
        """
        TC001: Verify GET /forecast returns current weather for multiple cities

        Validations:
        - Status code is 200
        - Response is valid JSON
        - Contains current weather data
        - Temperature is within reasonable range
        - Wind speed is non-negative
        """
        logger.info(f"TC001: Testing current weather for {city_name}")

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m",
        }

        response = api_client.get(OpenMeteoAPIConfig.FORECAST_ENDPOINT, params=params)

        validator.validate_status_code(response, 200)
        validator.validate_response_time(response)
        validator.validate_json_response(response)

        data = response.json()

        assert "current" in data, "Response should contain 'current' field"
        assert "temperature_2m" in data["current"], "Temperature field missing"
        assert "wind_speed_10m" in data["current"], "Wind speed field missing"

        temperature = data["current"]["temperature_2m"]
        wind_speed = data["current"]["wind_speed_10m"]

        assert (
            -50 <= temperature <= 50
        ), f"Temperature {temperature}°C seems unrealistic"
        assert wind_speed >= 0, f"Wind speed cannot be negative: {wind_speed}"

        logger.info(
            f"✓ {city_name}: Temperature={temperature}°C, Wind={wind_speed} km/h"
        )

    def test_get_hourly_forecast(self, api_client, validator, logger):
        """
        TC002: Verify hourly forecast endpoint

        Validations:
        - Status code is 200
        - Response contains hourly data
        - Hourly arrays have data
        """
        logger.info("TC002: Testing hourly forecast for Nuremberg")

        params = {
            "latitude": OpenMeteoAPIConfig.NUREMBERG_LAT,
            "longitude": OpenMeteoAPIConfig.NUREMBERG_LON,
            "hourly": "temperature_2m,precipitation",
        }

        response = api_client.get(OpenMeteoAPIConfig.FORECAST_ENDPOINT, params=params)

        validator.validate_status_code(response, 200)
        validator.validate_response_time(response)
        validator.validate_json_response(response)

        data = response.json()

        assert "hourly" in data, "Response should contain hourly data"
        assert "time" in data["hourly"], "Hourly should have time array"
        assert len(data["hourly"]["time"]) > 0, "Should have hourly data points"

        logger.info(f"✓ Hourly forecast: {len(data['hourly']['time'])} data points")

    def test_get_daily_forecast(self, api_client, validator, logger):
        """
        TC003: Verify daily forecast endpoint

        Validations:
        - Status code is 200
        - Response contains daily data
        - Contains max and min temperatures
        """
        logger.info("TC003: Testing daily forecast for Nuremberg")

        params = {
            "latitude": OpenMeteoAPIConfig.NUREMBERG_LAT,
            "longitude": OpenMeteoAPIConfig.NUREMBERG_LON,
            "daily": "temperature_2m_max,temperature_2m_min",
        }

        response = api_client.get(OpenMeteoAPIConfig.FORECAST_ENDPOINT, params=params)

        validator.validate_status_code(response, 200)
        validator.validate_response_time(response)
        validator.validate_json_response(response)

        data = response.json()

        assert "daily" in data, "Response should contain daily data"
        assert "temperature_2m_max" in data["daily"], "Should have max temperature"
        assert "temperature_2m_min" in data["daily"], "Should have min temperature"

        logger.info(f"✓ Daily forecast: {len(data['daily']['time'])} days")

    def test_invalid_coordinates(self, api_client, validator, logger):
        """
        TC004: Verify API returns 400 for invalid coordinates (Negative test)

        Validations:
        - Status code is 400 Bad Request
        - API handles invalid input gracefully
        """
        logger.info("TC004: Testing invalid coordinates")

        params = {
            "latitude": 999,  # Invalid (must be -90 to 90)
            "longitude": 999,  # Invalid (must be -180 to 180)
            "current": "temperature_2m",
        }

        response = api_client.get(OpenMeteoAPIConfig.FORECAST_ENDPOINT, params=params)

        validator.validate_status_code(response, 400)

        logger.info("✓ API correctly returned 400 for invalid coordinates")

    def test_invalid_endpoint(self, api_client, validator, logger):
        """
        TC005: Verify API returns 404 for non-existent endpoints (Negative test)

        Validations:
        - Status code is 404 Not Found
        - API handles routing errors gracefully
        """
        logger.info("TC005: Testing invalid endpoint handling")

        params = {
            "latitude": OpenMeteoAPIConfig.NUREMBERG_LAT,
            "longitude": OpenMeteoAPIConfig.NUREMBERG_LON,
            "current": "temperature_2m",
        }

        # Use wrong endpoint
        response = api_client.get("/v1/invalid_endpoint", params=params)

        validator.validate_status_code(response, 404)

        logger.info("✓ API correctly returned 404 for invalid endpoint")
