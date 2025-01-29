from loguru import logger
import sys
from services.weather_service.src.weather_service.core.config import settings
import json
#from loguru import logger as loguru_logger  # Accessing the global logger instance

def get_logger(name: str) -> logger :#loguru_logger.__class__:
    """
    Create and configure a logger instance using loguru with JSON logging and pretty print.

    Args:
        name (str): The name of the logger.

    Returns:
        Logger: Configured loguru logger instance.
    """

    # Remove default handler to avoid duplicate handlers
    logger.remove()

    # Set the log level from settings or default to INFO
    log_level = settings.LOG_LEVEL if hasattr(settings, "LOG_LEVEL") else "INFO"
    logger.level(log_level.upper())  # Set the level globally for all messages

    # Add stream handler with a formatted output
    if settings.PROJECT_NAME == "production":
        # JSON formatter for production environment
        logger.add(sys.stdout, format="{extra}", level="INFO")
    else:
        # Prettified human-readable output for development
        logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {extra}", level="DEBUG")

    return logger

# Prettified JSON formatting helper function (optional, for easier debug output)
def json_pretty_print(log_dict):
    return json.dumps(log_dict, indent=4)
