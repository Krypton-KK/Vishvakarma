
from fastapi import FastAPI
from app.routers import health, data
from app.utils.custom_logging import configure_logging
from app.config import settings

configure_logging()

app = FastAPI(title=settings.APP_NAME)

app.include_router(health.router)
app.include_router(data.router)
