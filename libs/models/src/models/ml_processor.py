import numpy as np
from libs.utils.src.utils.logger import get_logger

logger = get_logger(__name__)

def preprocess_weather_data(weather_data: dict) -> np.ndarray:
    """
    Process raw weather data into a feature vector for AI/ML models.

    Args:
        weather_data (dict): The raw weather data from the API.

    Returns:
        np.ndarray: Preprocessed feature vector.
    """
    logger.info(f"weather_data : {weather_data}")
    try:
        # Extract temperature in Celsius
        temp_celsius = weather_data.get("main", {}).get("temp", None)
        logger.info(f"function - libs.models.src.models.preprocess_weather_data => temp celsius : {temp_celsius}")
        if temp_celsius is None:
            logger.warning("function - libs.models.src.models.preprocess_weather_data => Temperature data missing; defaulting to 0°C.")
            temp_celsius = 273.15  # Default to 0°C in Kelvin
        #temp_celsius -= 273.15

        # Check for bad weather conditions
        weather_condition = weather_data.get("weather", [{}])[0].get("main", "").lower()
        logger.info(f"function - libs.models.src.models.preprocess_weather_data => weather_condition : {weather_condition}")
        is_bad_weather = 1 if weather_condition in ["rain", "snow", "storm"] else 0

        return np.array([temp_celsius, is_bad_weather])
    except Exception as e:
        logger.error(f"function - libs.models.src.models.preprocess_weather_data => Error preprocessing weather data: {e}")
        raise ValueError("Invalid weather data format") from e

def make_decision(feature_vector: np.ndarray) -> str:
    """
    Make a decision based on the feature vector.

    Args:
        feature_vector (np.ndarray): Preprocessed weather feature vector.

    Returns:
        str: "Yes" if the user can go out, "No" otherwise.
    """
    logger.info(f"function - libs.models.src.models.weather_decision => featuer_vector : {feature_vector}")
    try:
        temp, is_bad_weather = feature_vector
        if is_bad_weather:
            return "No"
        return "Yes"
    except Exception as e:
        logger.error(f"function - libs.models.src.models.weather_decision => Error in decision-making process: {e}")
        raise ValueError("Invalid feature vector format") from e