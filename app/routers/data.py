
from fastapi import APIRouter
from typing_extensions import deprecated
from fastapi import Request
from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.connectors.analytics_connector import AnalyticsConnector
from app.utils.limiter import limiter
from app.models.common import DataResponse, Metadata, SourcePayload
from datetime import datetime

from app.models.domain_models import SourcePayloadCRM, SourcePayloadSupport, SourcePayloadAnalytics

router = APIRouter()

@router.get("/data/crm", response_model=DataResponse)
@limiter.limit("5/minute")
def get_data_crm(request: Request, payload: SourcePayloadCRM):
    """
        Query customer by filter value of the specified filter parameter and return filtered customer list in sorted order according to the value of sortAscending.
        Gets only the top k values as specified by returnCount.

        Args:\n
            filterParameter: The field to filter by. Allowed: "customer_id", "name", "email", "created_at", "status".\n
            filterValue: The value to match. Allowed: string (for "name", "created_at", "status") or integer (for "customer_id") or EmailStr (for "email").\n
            returnCount: Number of results to return. Allowed integer (returns {settings.MAX_RESULTS = 10} results by default).\n
            sortAscending: Sort direction. True is for ascending and False for descending (default True).\n
    """
    connector = CRMConnector()
    return getter(connector, payload)

@router.get("/data/support", response_model=DataResponse)
@limiter.limit("5/minute")
def get_data_support(request: Request, payload: SourcePayloadSupport):
    """
        Query support_tickets by filter value of the specified filter parameter and return filtered customer list in sorted order according to the value of sortAscending.
        Gets only the top k values as specified by returnCount.

        Args:\n
            filterParameter: The field to filter by. Allowed: "ticket_id", "customer_id", "subject", "priority", "created_at", "status".\n
            filterValue: The value to match. Allowed: string (for "subject", "priority", "created_at", "status") or integer (for "ticket_id", "customer_id").\n
            returnCount: Number of results to return. Allowed integer (default {settings.MAX_RESULTS = 10}).\n
            sortAscending: Sort direction. True is for ascending and False for descending (default True).\n
    """
    connector = SupportConnector()
    return getter(connector, payload)

@router.get("/data/analytics", response_model=DataResponse)
@limiter.limit("5/minute")
def get_data_analytics(request: Request, payload: SourcePayloadAnalytics):
    """
        Query analytics by filter value of the specified filter parameter and return filtered analytics list in sorted order according to the value of sortAscending.
        Gets only the top k values as specified by returnCount.

        Args:\n
            filterParameter: The field to filter by. Allowed: "metric", "date", "value".\n
            filterValue: The value to match. Allowed: string (for "metric", "date") or integer (for "value").\n
            returnCount: Number of results to return. Allowed integer (returns {settings.MAX_RESULTS = 10} results by default).\n
            sortAscending: Sort direction. True is for ascending and False for descending (default True).\n
    """
    connector = AnalyticsConnector()
    return getter(connector, payload)

@router.get("/data/{other_path:path}", response_model=DataResponse)
@limiter.limit("5/minute")
def get_data_malformed(request: Request, other_path: str, payload: SourcePayload):
    """
    All other endpoints those return wrong or malformed data.

    Args:\n
        payload: SourcePayload\n
    """
    return DataResponse(data=[], metadata=Metadata(total_results=0, returned_results=0, data_freshness="unknown", summary=""))


def getter(connector: CRMConnector | AnalyticsConnector | SupportConnector, payload: SourcePayloadCRM | SourcePayloadAnalytics | SourcePayloadSupport):
    raw_total = connector.raw_size
    print(f"total entries in the json file: {raw_total}")

    optimized = connector.query(payload.filterParameter,
                                payload.filterValue,
                                payload.returnCount,
                                payload.sortAscending)

    metadata = Metadata(
        total_results=optimized[2], # the no of results the query got
        returned_results=len(optimized), # the no of results optimized for the ai model
        data_freshness=f"Data as of {datetime.utcnow().isoformat()}",
        summary=optimized[1] # summary string which has both the total and the returned
    )

    return DataResponse(data=optimized[0], metadata=metadata)


@deprecated("use get_data_support or get_data_analytics or get_data_crm instead")
def get_data_old(source: str, payload: SourcePayload):

    # connector_map = {
    #     "crm": CRMConnector(),
    #     "support": SupportConnector(),
    #     "analytics": AnalyticsConnector(),
    # }
    #
    # connector = connector_map.get(source)
    # if not connector:
    #     return {"data": [], "metadata": {"total_results": 0, "returned_results": 0, "data_freshness": "unknown"}}

    # Lazy loading !
    if (source == "crm"):
        connector = CRMConnector()
    elif (source == "support"):
        connector = SupportConnector()
    elif (source == "analytics"):
        connector = AnalyticsConnector()
    else:
        return {"data": [], "metadata": {"total_results": 0, "returned_results": 0, "data_freshness": "unknown"}}

    raw_total = connector.raw_size
    print(f"total entries in the json file: {raw_total}")

    optimized = connector.query(payload.filterParameter,
                                payload.filterValue,
                                payload.returnCount,
                                payload.sortAscending)

    metadata = Metadata(
        total_results=optimized[2], # the no of results the query got
        returned_results=len(optimized), # the no of results optimized for the ai model
        data_freshness=f"Data as of {datetime.utcnow().isoformat()}",
        summary=optimized[1] # summary string which has both the total and the returned
    )

    return DataResponse(data=optimized[0], metadata=metadata)
