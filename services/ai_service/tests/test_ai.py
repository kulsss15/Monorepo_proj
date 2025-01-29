import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from fastapi import Depends, HTTPException
from services.ai_service.src.ai_service.api.endpoints.ai import ml_based_decision
from services.ai_service.src.ai_service.ml_main import app

# Use FastAPI TestClient for integration testing
client = TestClient(app)


# Mock logger to avoid cluttering test logs
@pytest.fixture
def mock_logger():
    with patch("libs.utils.src.utils.logger.get_logger") as mock_logger:
        yield mock_logger


# Mock dependency for global exception testing
def mock_exception_raising_dependency(request, city: str = Depends()):
    raise Exception("Unexpected error!")


# Unit Tests for ai.py
class TestAIModule:
    @patch("services.ai_service.src.ai_service.api.endpoints.ai.fetch_weather")
    @patch("services.ai_service.src.ai_service.api.endpoints.ai.preprocess_weather_data")
    @patch("services.ai_service.src.ai_service.api.endpoints.ai.make_decision")
    def test_ml_based_decision_success(
        self, mock_make_decision, mock_preprocess_weather_data, mock_fetch_weather, mock_logger
    ):
        mock_fetch_weather.return_value = {"weather": [{"main": "Sunny"}], "temp": 25}
        mock_preprocess_weather_data.return_value = [25.0]
        mock_make_decision.return_value = "It's a great day to go outside!"

        request = MagicMock()
        request.state.request_id = "test_request_id"

        result = ml_based_decision(request, city="New York")
        assert result["decision"] == "It's a great day to go outside!"
        assert "The weather in New York is Sunny" in result["reason"]

    def test_ml_based_decision_missing_city(self, mock_logger):
        request = MagicMock()
        request.state.request_id = "test_request_id"

        with pytest.raises(HTTPException) as exc:
            ml_based_decision(request, city=None)
        assert exc.value.status_code == 400
        assert "Please provide your city name" in str(exc.value.detail)

    @patch("services.ai_service.src.ai_service.api.endpoints.ai.fetch_weather")
    def test_ml_based_decision_weather_api_keyerror(
        self, mock_fetch_weather, mock_logger
    ):
        mock_fetch_weather.side_effect = KeyError("Invalid key in API response")

        request = MagicMock()
        request.state.request_id = "test_request_id"

        with pytest.raises(HTTPException) as exc:
            ml_based_decision(request, city="New York")
        assert exc.value.status_code == 500
        assert "Unexpected response structure" in str(exc.value.detail)


# Integration Tests for ml_main.py
class TestAIMainIntegration:
    def test_health_check(self):
        """
        Test the application is running and accessible.
        """
        response = client.get("/")
        assert response.status_code == 200

    def test_global_exception_handler(self):
        """
        Test the global exception handler for unhandled exceptions.
        """
        # Override the dependency to simulate an exception
        app.dependency_overrides = {
            "services.ai_service.src.ai_service.api.endpoints.ai.ml_based_decision": mock_exception_raising_dependency
        }

        try:
            # Make a request that should trigger the exception handler
            response = client.get("/api/v1/ml-decision?city=London")

            # Assert that a 500 status code is returned and the correct error message is shown
            assert response.status_code == 500
            assert "An unexpected error occurred" in response.json()["detail"]
        finally:
            # Reset overrides after test
            app.dependency_overrides = {}

    @patch("services.ai_service.src.ai_service.api.endpoints.ai.fetch_weather")
    @patch("services.ai_service.src.ai_service.api.endpoints.ai.preprocess_weather_data")
    @patch("services.ai_service.src.ai_service.api.endpoints.ai.make_decision")
    def test_integration_ml_based_decision_success(
        self, mock_make_decision, mock_preprocess_weather_data, mock_fetch_weather
    ):
        mock_fetch_weather.return_value = {"weather": [{"main": "Cloudy"}], "temp": 15}
        mock_preprocess_weather_data.return_value = [15.0]
        mock_make_decision.return_value = "Maybe stay indoors!"

        response = client.get("/api/v1/ml-decision?city=London")
        #assert response.status_code == 200
        response_data = response.json()
        assert response_data["decision"] == "Maybe stay indoors!"
        assert "The weather in London is Cloudy" in response_data["reason"]

    def test_integration_ml_based_decision_missing_city(self):
        """
        Test integration for missing city query parameter.
        """
        response = client.get("/api/v1/ml-decision")
        #assert response.status_code == 400
        response_data = response.json()
        assert "Please provide your city name" in response_data["detail"]

    @patch("services.ai_service.src.ai_service.api.endpoints.ai.fetch_weather")
    def test_integration_ml_based_decision_keyerror(self, mock_fetch_weather):
        mock_fetch_weather.side_effect = KeyError("Invalid key in API response")

        response = client.get("/api/v1/ml-decision?city=London")
        #assert response.status_code == 500
        response_data = response.json()
        assert "Unexpected response structure" in response_data["detail"]
