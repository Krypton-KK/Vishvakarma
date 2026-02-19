from fastapi import FastAPI, Security
from app.utils.limiter import limiter
from app.utils.custom_logging import configure_logging
from app.config import settings
from app.utils.security import get_api_key
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

configure_logging()
app = FastAPI(title=settings.APP_NAME)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
from app.routers import health, data
app.include_router(data.router, dependencies=[Security(get_api_key)])
app.include_router(health.router)
