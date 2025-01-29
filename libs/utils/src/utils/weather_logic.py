from typing import Dict
from fastapi import HTTPException
from libs.utils.src.utils.api_client import fetch_weather
from libs.utils.src.utils.logger import get_logger

logger = get_logger(__name__)

def process_weather_decision(weather_data: Dict, city: str) -> Dict:
    """
    Process weather data and determine if it's a good idea to go out.

    Args:
        weather_data (dict): The raw weather data from the API.
        city (str): The city for which weather data was fetched.

    Returns:
        dict: A dictionary containing the decision and the reason.
    """
    # Extract relevant data
    weather_main = weather_data.get("weather", [{}])[0].get("main", "").lower()
    temp = weather_data.get("main", {}).get("temp")
    feels_like = weather_data.get("main", {}).get("feels_like")
    logger.info(f"function - libs.utils.src.utils.weather_logic.process_weather_decision => weather_main: {weather_main}, temp: {temp}, feels_like : {feels_like}")
    # Default decision template
    decision = {"decision": "Yes", "reason": f"The weather in {city} is clear and suitable to go out."}

    # Decision logic based on weather conditions
    if weather_main in ["rain", "snow", "storm"]:
        decision["decision"] = "No"
        decision["reason"] = f"The weather in {city} is {weather_main}, not ideal to go out."
    elif temp is not None and temp < 5:  # Temperature threshold
        decision["decision"] = "No"
        decision["reason"] = f"The temperature in {city} is {temp}°C, which is too cold to go out."
    elif feels_like is not None and feels_like < 5:  # Feels-like temperature threshold
        decision["decision"] = "No"
        decision["reason"] = f"The 'feels-like' temperature in {city} is {feels_like}°C, making it uncomfortable to go out."

    return decision

def should_go_out(api_key: str, city: str) -> Dict:
    """
    Fetch weather data and determine if it's a good idea to go out.

    Args:
        api_key (str): API key for accessing the weather API.
        city (str): The city for which to fetch weather data.

    Returns:
        dict: A dictionary containing the decision and the reason.

    Raises:
        HTTPException: If the API key is not configured or if there's an error fetching weather data.
    """
    logger.info(f"function - libs.utils.src.utils.env_loader.should_go_out => api_key : {api_key} & city : {city}")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key is not configured or missing.")
    try:
        # Fetch weather data
        weather_data = fetch_weather(api_key, city)
        # Process decision based on weather data
        return process_weather_decision(weather_data, city)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching or processing weather data: {str(e)}")
