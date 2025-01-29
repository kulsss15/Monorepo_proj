from fastapi import APIRouter, HTTPException, Request, Query
from libs.utils.src.utils.api_client import fetch_weather  # Update import path for utils
from libs.models.src.models.ml_processor import preprocess_weather_data, make_decision  # Update import path
from libs.utils.src.utils.logger import get_logger  # Update import path
from libs.utils.src.utils.env_loader import settings  # Update import path

router = APIRouter()
logger = get_logger(__name__)

@router.get("/ml-decision")
def ml_based_decision(
    request: Request,
    city: str = Query(
        None, 
        description="Enter the name of your city to get weather-based AI decisions."
    ),
):
    """
    Make an AI-based decision on whether to go out based on weather data.
    Ensures the temperature is returned in Celsius.

    Args:
        request (Request): The current request object for tracing and context.
        city (str): Name of the city (prompted if not provided).

    Returns:
        dict: Decision and reasoning.
    """
    request_id = request.state.request_id

    # Ensure city is provided
    if not city:
        logger.warning("City parameter is missing", extra={"request_id": request_id})
        raise HTTPException(
            status_code=400,
            detail="Please provide your city name to get the decision."
        )

    api_key = settings.OPENWEATHER_API_KEY

    try:
        # Fetch weather data with metric units (Celsius)
        logger.info("Fetching weather data", extra={"request_id": request_id, "city": city})
        weather_data = fetch_weather(api_key, city)

        # Preprocess data for AI/ML
        logger.debug("Preprocessing weather data", extra={"request_id": request_id})
        features = preprocess_weather_data(weather_data)

        # Make an AI-based decision
        decision = make_decision(features)

        logger.info(
            "Decision made successfully",
            extra={"request_id": request_id, "decision": decision, "city": city},
        )

        return {
            "decision": decision,
            "reason": f"The weather in {city} is {weather_data['weather'][0]['main']}, "
                      f"temperature is {features[0]:.2f}°C.",
        }

    except KeyError as e:
        logger.error("KeyError while processing weather data", extra={"request_id": request_id, "error": str(e)})
        raise HTTPException(status_code=500, detail="Unexpected response structure from weather API.")

    except Exception as e:
        logger.error("Unhandled exception", extra={"request_id": request_id, "error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error processing request: {e}")
