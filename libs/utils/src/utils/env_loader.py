import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import ValidationError
from libs.utils.src.utils.logger import get_logger
from services.weather_service.src.weather_service.core.config import settings

logger = get_logger(__name__)


def load_env():
    """
    Load environment variables from a .env file.
    """
    load_dotenv()
    logger.info("Environment variables loaded from .env file.")

try:
    # Load environment variables and validate
    # settings = settings()
    # Access the API key in your application
    api_key = settings.OPENWEATHER_API_KEY
    logger.info("Environment variables successfully validated and loaded.")
except ValidationError as e:
    # Log detailed error message
    missing_vars = [err['loc'][0] for err in e.errors()]
    logger.error(
        f"Environment variables validation failed. Missing or invalid variables: {missing_vars}"
    )
    raise RuntimeError(f"Environment variables validation failed: {e}")