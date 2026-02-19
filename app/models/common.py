
from pydantic import BaseModel
from typing import Any, List, Literal

from app.config import settings

class Metadata(BaseModel):
    total_results: int
    returned_results: int
    data_freshness: str
    summary: str

class DataResponse(BaseModel):
    data: List[Any]
    metadata: Metadata

class SourcePayload(BaseModel):
    filterParameter: str
    filterValue: str | int
    returnCount: int = settings.MAX_RESULTS
    sortAscending: bool = True

