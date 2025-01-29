import os
import requests
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from services.weather_service.src.weather_service.main import app
###from libs.utils.src.utils.weather_logic import health_check_db, health_check_weather_api###

# Initialize TestClient for FastAPI app
client = TestClient(app)

# Mock Environment Variables
API_KEY = "5573debcbbc67c80c90a4bdbabe3504d" # Replace with a valid test API key for integration tests
os.environ["OPENWEATHER_API_KEY"] = API_KEY


"""# Helper function to mock database session
@pytest.fixture
def mock_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from services.weather_service.src.weather_service.db.models import Base

    # In-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()"""
@pytest.fixture
def api_url():
    return "https://api.opeweatherapi.com"  # Replace with actual URL

@pytest.fixture
def api_key():
    return "5573debcbbc67c80c90a4bdbabe3504d"  # Replace with your actual key or mock it

### UNIT TESTS ###

def test_should_go_out_success(mocker):
    """
    Test should_go_out with a mock API response.
    """
    mock_response = {
        "weather": [{"main": "Clear"}],
        "main": {"temp": 20, "feels_like": 18},
    }
    mocker.patch("libs.utils.src.utils.api_client.fetch_weather", return_value=mock_response)

    response = client.get("/api/v1/decision?city=London")
    assert response.status_code == 200
    assert response.json() == {
        "decision": "Yes",
        "reason": "The weather in London is clear and suitable to go out.",
    }


def test_should_go_out_bad_weather(mocker):
    """
    Test should_go_out with bad weather conditions.
    """
    mock_response = {
        "weather": [{"main": "Rain"}],
        "main": {"temp": 15, "feels_like": 13},
    }
    mocker.patch("libs.utils.src.utils.api_client.fetch_weather", return_value=mock_response)

    response = client.get("/api/v1/decision?city=London")
    assert response.status_code == 200
    assert response.json() == {
        "decision": "No",
        "reason": "The weather in London is rain, not ideal to go out.",
    }


def test_should_go_out_missing_api_key(mocker):
    """
    Test should_go_out when API key is missing.
    """
    mocker.patch.dict(os.environ, {"OPENWEATHER_API_KEY": ""})

    response = client.get("/api/v1/decision?city=London")
    assert response.status_code == 500
    assert response.json()["detail"] == "API key is not configured or missing."


def test_should_go_out_api_error(mocker):
    """
    Test should_go_out when API fetch fails.
    """
    mocker.patch("libs.utils.src.utils.api_client.fetch_weather", side_effect=Exception("API error"))

    response = client.get("/api/v1/decision?city=London")
    assert response.status_code == 500
    assert "Error fetching or processing weather data" in response.json()["detail"]


### INTEGRATION TESTS ###

def test_integration_should_go_out():
    """
    Integration test for should_go_out with live API.
    """
    response = client.get(f"/api/v1/decision?city=London")
    assert response.status_code == 200
    assert "decision" in response.json()
    assert "reason" in response.json()


""" HEALTH CHECK TESTS

def test_health_check_db(mock_session):
    
    ###Test database health check.###
    
    health_status = health_check_db(mock_session)
    assert health_status["status"] == "Healthy"
    assert health_status["service"] == "Database"


def test_health_check_weather_api_success():
    
    ###Test weather API health check with a valid API key.###
    
    health_status = health_check_weather_api(API_KEY)
    assert health_status["status"] == "Healthy"
    assert health_status["service"] == "OpenWeather API"


def test_health_check_weather_api_failure(mocker):
    
    ###Test weather API health check when the API key is invalid.###
    
    mocker.patch("requests.get", return_value=type("MockResponse", (), {"status_code": 401, "json": lambda: {"message": "Invalid API key"}})())
    health_status = health_check_weather_api("invalid_key")
    assert health_status["status"] == "Unhealthy"
    assert health_status["service"] == "OpenWeather API"
    assert "Invalid API key" in health_status["error"] 


def test_health_check_weather_api_connection_error(mocker):
    
    ##Test weather API health check when there's a connection error.##
    
    mocker.patch("requests.get", side_effect=Exception("Connection error"))
    health_status = health_check_weather_api(API_KEY)
    assert health_status["status"] == "Unhealthy"
    assert health_status["service"] == "OpenWeather API"
    assert "Connection error" in health_status["error"] """