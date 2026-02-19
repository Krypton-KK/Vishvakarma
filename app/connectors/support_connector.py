from typing_extensions import deprecated
from app.connectors.base import BaseConnector
from operator import attrgetter
from typing import List, Literal
from pydantic import TypeAdapter
from app.models.domain_models import Tickets
from pathlib import Path
from app.config import settings
from app.services.business_rules import apply_voice_limits
from app.services.voice_optimizer import summarize_if_large


class SupportConnector(BaseConnector):
    def __init__(self):
        ticketsAdapter = TypeAdapter(List[Tickets])
        ticketsJson = Path(f'{settings.APP_DIR}/../data/support_tickets.json').read_text()
        self.ticketsList = ticketsAdapter.validate_json(ticketsJson)
        self.raw_size = len(self.ticketsList)

    @deprecated("use query() instead")
    def fetch(self, **kwargs):
        data, summary, size = self.query(
            filterParameter=kwargs.get('filter_param'),
            filterValue=kwargs.get('filter_value'),
            returnCount=kwargs.get('limit', 5),
            sortAscending=kwargs.get('sortAscending', True)
        )
        return data

    def query(self,
              filterParameter: Literal["ticket_id", "customer_id", "subject", "priority", "created_at","status"],
              filterValue: str | int,
              returnCount: int = 5,
              sortAscending: bool = True) -> tuple[list[Tickets], str, int]:
        f"""
        Query support_tickets by filter value of the specified filter parameter and return filtered customer list in sorted order according to the value of sortAscending.
        Gets only the top k values as specified by returnCount.

        Args:
            filterParameter: The field to filter by. Allowed: "ticket_id", "customer_id", "subject", "priority", "created_at", "status".
            filterValue: The value to match. Allowed: string (for "subject", "priority", "created_at", "status") or integer (for "ticket_id", "customer_id").
            returnCount: Number of results to return. Allowed integer (default {settings.MAX_RESULTS}).
            sortAscending: Sort direction. True is for ascending and False for descending (default True).
        """
        # filter the List[Tickets]
        filtered = [
            c for c in self.ticketsList
            if getattr(c, filterParameter, None) == filterValue
        ]
        # sort the filtered output
        filtered.sort(
            key=attrgetter(filterParameter),
            reverse=not sortAscending
        )
        # return top k values and total values that are present...
        return apply_voice_limits(filtered, returnCount), summarize_if_large(filtered,filterParameter), len(filtered)
