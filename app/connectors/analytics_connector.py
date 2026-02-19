from typing_extensions import deprecated
from app.connectors.base import BaseConnector
from operator import attrgetter
from typing import List, Literal
from pydantic import TypeAdapter, EmailStr
from app.models.domain_models import Analytics
from pathlib import Path
from app.config import settings
from app.services.business_rules import apply_voice_limits
from app.services.voice_optimizer import summarize_if_large


class AnalyticsConnector(BaseConnector):
    def __init__(self):
        analyticsAdapter = TypeAdapter(List[Analytics])
        analyticsJson = Path(f'{settings.APP_DIR}/../data/analytics.json').read_text()
        self.analyticsList = analyticsAdapter.validate_json(analyticsJson)
        self.raw_size = len(self.analyticsList)

    @deprecated("use query() instead")
    def fetch(self, **kwargs):
        data, summary, total = self.query(
            filterParameter=kwargs.get('filter_param'),
            filterValue=kwargs.get('filter_value'),
            returnCount=kwargs.get('limit', 5),
            sortAscending=kwargs.get('sortAscending', True)
        )
        return data

    def query(self,
              filterParameter: Literal["metric", "date", "value"],
              filterValue: str | int,
              returnCount: int = settings.MAX_RESULTS,
              sortAscending: bool = True) -> tuple[list[Analytics], str, int]:
        f"""
        Query analytics by filter value of the specified filter parameter and return filtered analytics list in sorted order according to the value of sortAscending.
        Gets only the top k values as specified by returnCount.

        Args:
            filterParameter: The field to filter by. Allowed: "metric", "date", "value".
            filterValue: The value to match. Allowed: string (for "metric", "date") or integer (for "value").
            returnCount: Number of results to return. Allowed integer (returns {settings.MAX_RESULTS} results by default).
            sortAscending: Sort direction. True is for ascending and False for descending (default True).
        """
        # filter the List[Analytics]
        filtered = [
            c for c in self.analyticsList
            if getattr(c, filterParameter, None) == filterValue
        ]
        # sort the filtered output
        filtered.sort(
            key=attrgetter(filterParameter),
            reverse=not sortAscending
        )
        # return top k values and total values that are present...
        return apply_voice_limits(filtered, returnCount), summarize_if_large(filtered, filterParameter), len(filtered)
