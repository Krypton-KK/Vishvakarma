from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
client = TestClient(app)

def test_health_check():
    """Verify that the health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_crm_data_valid():
    """
    Test fetching CRM data with valid filters.
    NOTE: Using GET with JSON body as currently implemented in the API.
    """
    payload = {
        "filterParameter": "status",
        "filterValue": "active",
        "returnCount": 5,
        "sortAscending": True
    }
    response = client.request("GET", "/data/crm", headers={"x-api-key": settings.API_KEY[0]}, json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "data" in data
    assert "metadata" in data

    results = data["data"]
    assert isinstance(results, list)
    if len(results) > 0:
        assert results[0]["status"] == "active"

def test_get_crm_data_limit():
    """Test that returnCount actually limits results."""
    limit = 2
    payload = {
        "filterParameter": "status",
        "filterValue": "active",
        "returnCount": limit
    }
    response = client.request("GET", "/data/crm", headers={"x-api-key": settings.API_KEY[0]}, json=payload)
    assert response.status_code == 200
    assert len(response.json()["data"]) <= limit

def test_get_support_data_priority():
    """Test fetching support tickets by priority."""
    payload = {
        "filterParameter": "priority",
        "filterValue": "high",
        "returnCount": 5
    }
    response = client.request("GET", "/data/support", headers={"x-api-key": settings.API_KEY[0]}, json=payload)
    assert response.status_code == 200
    results = response.json()["data"]

    if len(results) > 0:
        assert results[0]["priority"] == "high"

def test_get_analytics_data():
    """Test fetching analytics data."""
    payload = {
        "filterParameter": "metric",
        "filterValue": "daily_active_users",
        "returnCount": 5
    }
    response = client.request("GET", "/data/analytics", headers={"x-api-key": settings.API_KEY[0]}, json=payload)
    assert response.status_code == 200

    results = response.json()["data"]

    if len(results) > 0:
        assert results[0]["metric"] == "daily_active_users"

def test_invalid_filter_param():
    """Test that invalid filter parameters result in 422 Validation Error."""
    payload = {
        "filterParameter": "INVALID_PARAM",
        "filterValue": "test"
    }
    response = client.request("GET", "/data/crm", headers={"x-api-key": settings.API_KEY[0]}, json=payload)
    assert response.status_code == 422


def test_malformed_endpoint():
    """Test the catch-all endpoint for malformed paths."""
    payload = {
        "filterParameter": "status",
        "filterValue": "active"
    }
    response = client.request("GET", "/data/nonexistent_resource", headers={"x-api-key": settings.API_KEY[0]}, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["metadata"]["total_results"] == 0
    assert data["data"] == []


def test_rate_limit():
    """Test that exceeds rate limit and results in 429 Too Many Requests."""
    for i in range(5):
        payload = {
            "filterParameter": "metric",
            "filterValue": "daily_active_users",
            "returnCount": 5
        }
        response = client.request("GET", "/data/analysis", headers={"x-api-key": settings.API_KEY[0]}, json=payload)
    # 6th one must respond with the 429 Too Many Requests status code
    payload = {
        "filterParameter": "metric",
        "filterValue": "daily_active_users",
        "returnCount": 5
    }
    response = client.request("GET", "/data/analysis", headers={"x-api-key": settings.API_KEY[0]}, json=payload)
    assert response.status_code == 429