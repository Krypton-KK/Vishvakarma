from typing_extensions import deprecated
from app.connectors.base import BaseConnector
from operator import attrgetter
from typing import List, Literal
from pydantic import TypeAdapter, EmailStr
from app.models.domain_models import Customer
from pathlib import Path
from app.config import settings
from app.services.business_rules import apply_voice_limits
from app.services.voice_optimizer import summarize_if_large


class CRMConnector(BaseConnector):
    def __init__(self):
        customerAdapter = TypeAdapter(List[Customer])
        customerJson = Path(f'{settings.APP_DIR}/../data/customers.json').read_text()
        self.customerList = customerAdapter.validate_json(customerJson)
        self.raw_size = len(self.customerList)

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
              filterParameter: Literal["customer_id", "name", "email", "created_at", "status"],
              filterValue: str | int | EmailStr,
              returnCount: int = settings.MAX_RESULTS,
              sortAscending: bool = True) -> tuple[list[Customer], str, int]:
        f"""
        Query customer by filter value of the specified filter parameter and return filtered customer list in sorted order according to the value of sortAscending.
        Gets only the top k values as specified by returnCount.

        Args:
            filterParameter: The field to filter by. Allowed: "customer_id", "name", "email", "created_at", "status".
            filterValue: The value to match. Allowed: string (for "name", "created_at", "status") or integer (for "customer_id") or EmailStr (for "email").
            returnCount: Number of results to return. Allowed integer (returns {settings.MAX_RESULTS} results by default).
            sortAscending: Sort direction. True is for ascending and False for descending (default True).
        """
        # filter the List[Customer]
        filtered = [
            c for c in self.customerList
            if getattr(c, filterParameter, None) == filterValue
        ]
        # sort the filtered output
        filtered.sort(
            key=attrgetter(filterParameter),
            reverse=not sortAscending
        )
        # return top k values and total values that are present...
        return apply_voice_limits(filtered, returnCount), summarize_if_large(filtered, filterParameter), len(filtered)
