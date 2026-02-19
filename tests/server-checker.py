import httpx

from app.config import settings

API_URL = "http://localhost:8000"
args = [
    {"filterParameter": "status", "filterValue": "active","returnCount": 15,"sortAscending": True}, # first 15 active
    {"filterParameter": "priority","filterValue": "low","returnCount": 3,"sortAscending": False}, # last 3 low priority tickets
    {"filterParameter": "metric","filterValue": "daily_active_users"} # gets the first 10 analytics posts
]

print("-------------------------------------------")

api_response = httpx.request(
    "GET",
    f"{API_URL}/health",
    headers={"x-api-key": settings.API_KEY[0]},
    json=None
)
print(api_response.json())

print("-------------------------------------------")

api_response = httpx.request(
    "GET",
    f"{API_URL}/data/crm",
    headers={"x-api-key": settings.API_KEY[0]},
    json=args[0]
)
print(api_response.json())

print("-------------------------------------------")

api_response = httpx.request(
    "GET",
    f"{API_URL}/data/support",
    headers={"x-api-key": settings.API_KEY[0]},
    json=args[1]
)
print(api_response.json())

print("-------------------------------------------")

api_response = httpx.request(
    "GET",
    f"{API_URL}/data/analytics",
    headers={"x-api-key": settings.API_KEY[0]},
    json=args[2]
)
print(api_response.json())

print("-------------------------------------------")

api_response = httpx.request(
    "GET",
    f"{API_URL}/data/",
    headers={"x-api-key": settings.API_KEY[0]},
    json=args[1]
)
print(api_response.json())

print("-------------------------------------------")