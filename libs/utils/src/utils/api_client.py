import requests
from typing import Dict
from libs.utils.src.utils.logger import get_logger
from services.weather_service.src.weather_service.core.config import settings

logger = get_logger(__name__)

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def fetch_weather(api_key: str, city: str) -> Dict:
    """
    Fetch weather data for a given city from the OpenWeatherMap API.

    Args:
        api_key (str): API key for OpenWeatherMap.
        city (str): Name of the city.

    Returns:
        Dict: Parsed JSON response from the API.

    Raises:
        ValueError: If the city name is invalid.
        HTTPError: If the API response contains an error.
        RequestException: For other network-related issues.
    """

    if not city or not city.strip():
        logger.error("City name is required but was not provided.")
        raise ValueError("City name cannot be empty.")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",  # Fetch temperature in Celsius
    }

    try:
        logger.info("Fetching weather data for city: %s", city)
        logger.info("Using API key: %s", api_key)
        response = requests.get(
            BASE_URL, params=params, timeout=10
        )  # Set timeout to 10 seconds
        response.raise_for_status()
        data = response.json()
        logger.info("Weather data fetched successfully for city: %s", city)
        return data
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred: %s", http_err)
        raise
    except requests.exceptions.RequestException as req_err:
        logger.error("Request exception occurred: %s", req_err)
        raise
    except Exception as e:
        logger.error("Unexpected error occurred while fetching weather data: %s", e)
        raise