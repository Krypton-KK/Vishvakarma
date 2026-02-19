
from typing import List, Dict
from app.config import settings
from app.models.domain_models import Customer, Tickets, Analytics
from app.services.data_identifier import identify_data


def summarize_if_large(data: list[Customer | Analytics | Tickets], datatype: str) -> str:
    if len(data) > settings.MAX_RESULTS:
        return f"summary: {len(data)} records found. Showing first {settings.MAX_RESULTS} records. It is {identify_data(datatype, data)} data."
    return f"summary: {len(data)} records found. Showing all fetched records. It is {identify_data(datatype, data)} data."
