"""
Tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test suite for API endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "MA EV ChargeMap" in data["name"]
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "database" in data
    
    def test_get_cities(self):
        """Test getting list of cities."""
        response = client.get("/api/cities")
        assert response.status_code == 200
        
        cities = response.json()
        assert isinstance(cities, list)
        assert len(cities) > 0
        
        # Check Worcester is included
        worcester = next((c for c in cities if c["slug"] == "worcester"), None)
        assert worcester is not None
        assert worcester["name"] == "Worcester"
        assert worcester["state"] == "MA"
        assert "bbox" in worcester
        assert "center" in worcester
    
    def test_get_city_by_slug(self):
        """Test getting specific city info."""
        response = client.get("/api/cities/worcester")
        assert response.status_code == 200
        
        city = response.json()
        assert city["slug"] == "worcester"
        assert city["name"] == "Worcester"
    
    def test_get_city_not_found(self):
        """Test getting non-existent city returns 404."""
        response = client.get("/api/cities/nonexistent")
        assert response.status_code == 404
    
    def test_predict_endpoint(self):
        """Test ML prediction endpoint."""
        request_data = {
            "traffic_index": 0.7,
            "pop_density_index": 0.6,
            "renters_share": 0.5,
            "income_index": 0.4,
            "poi_index": 0.65,
            "parking_lot_flag": 1,
            "municipal_parcel_flag": 0
        }
        
        response = client.post("/api/predict", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "scores" in data
        assert "daily_kwh_estimate" in data
        assert "model_info" in data
        
        # Check score structure
        scores = data["scores"]
        assert "demand" in scores
        assert "equity" in scores
        assert "traffic" in scores
        assert "grid" in scores
        assert "overall" in scores
        
        # Check values are in valid ranges
        for score_name, score_value in scores.items():
            assert 0 <= score_value <= 100, f"{score_name} out of range"
        
        assert data["daily_kwh_estimate"] > 0
    
    def test_predict_endpoint_validation(self):
        """Test prediction endpoint validates input ranges."""
        # Test with out-of-range value
        request_data = {
            "traffic_index": 1.5,  # Invalid: > 1.0
            "pop_density_index": 0.6,
            "renters_share": 0.5,
            "income_index": 0.4,
            "poi_index": 0.65,
        }
        
        response = client.post("/api/predict", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_openapi_schema(self):
        """Test that OpenAPI schema is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Check that we can get the schema
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
