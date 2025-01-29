from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.weather_service.src.weather_service.core.config import settings
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Create the database engine with additional options
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using them
    pool_size=10,  # Maximum number of connections in the pool
    max_overflow=20,  # Additional connections allowed beyond pool_size
    pool_timeout=30,  # Timeout for getting a connection from the pool
    echo=False,  # Set to True for debugging SQL queries
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency injection for FastAPI
def get_db():
    """
    Dependency for database session management.
    Ensures sessions are properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()