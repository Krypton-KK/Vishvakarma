
from fastapi import FastAPI, Security
from app.utils.custom_logging import configure_logging
from app.config import settings
from app.utils.security import get_api_key

configure_logging()
app = FastAPI(title=settings.APP_NAME)

from app.routers import health, data
app.include_router(data.router, dependencies=[Security(get_api_key)])
app.include_router(health.router)
