from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from libs.utils.src.utils.weather_logic import should_go_out
from services.weather_service.src.weather_service.core.config import settings
from libs.utils.src.utils.logger import get_logger
from libs.utils.src.utils.api_client import fetch_weather

router = APIRouter()
logger = get_logger(__name__)


class WeatherResponse(BaseModel):
    temperature: float
    condition: str
    description: str
    decision: str
    advice: str


@router.get("/weather", response_model=WeatherResponse)
def get_weather(api_key, city: str = Query(..., min_length=1, examples="London")):
    """
    Fetch weather data for a given city and make a go-out decision.

    Args:
        city (str): Name of the city.

    Returns:
        WeatherResponse: Weather details and decision.
    """
    #api_key = settings.OPENWEATHER_API_KEY

    try:
        # Fetch weather data and process the decision using the new logic
        decision_data = should_go_out(api_key, city)
        # Fetch the weather data again for the response details
        weather_data = fetch_weather(api_key, city)
        temp = weather_data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
        condition = weather_data["weather"][0]["main"]
        description = weather_data["weather"][0]["description"]
        # Use the decision from the weathr_logic
        decision = decision_data["decision"]
        advice = decision_data["reason"]
        logger.info(f"function - api.endpoints.weather.get_weather => temp : {temp}, condition : {condition}, description : {description}")
        return WeatherResponse(
            temperature=round(temp, 2),
            condition=condition,
            description=description.capitalize(),
            decision=decision,
            advice=advice,
        )
    except Exception as e:
        logger.error(f"function - api.endpoints.weather.get_weather => Error fetching weather for city {city}: {str(e)}")
        raise HTTPException(
            status_code=400, detail="Failed to fetch weather data. Please try again."
        )