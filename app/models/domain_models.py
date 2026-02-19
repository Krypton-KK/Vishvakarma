
from pydantic import BaseModel, EmailStr
from typing import List, Literal
from app.models.common import DataResponse, SourcePayload


# Analytics.json Structure
#  {
#     "metric": "daily_active_users",
#     "date": "2026-02-16",
#     "value": 872
#   },

class Analytics(BaseModel):
    """
    the data model for analytics.json
    """
    metric : str
    date: str
    value:  int

class AnalyticsResponse(DataResponse):
    """
        special response model for analytics so that it is easy for
        us and the LLM to distinguish it from the support ticket and customer response models
    """
    data: List[Analytics]

# Customers.json Structure
#  {
#     "customer_id": 1,
#     "name": "Customer 1",
#     "email": "user1@example.com",
#     "created_at": "2025-03-03T03:46:48.375649",
#     "status": "active"
#   },

class Customer(BaseModel):
    """
    the data model for customer.json
    """
    customer_id: int
    name: str
    email: EmailStr # using the pydantic model for better typesafety
    created_at: str
    status: Literal["active","inactive"]

class CustomerResponse(DataResponse):
    """
    special response model for customer so that it is easy for
    us and the LLM to distinguish it from the support ticket and analytics response models
    """
    data: List[Customer]

# Support Tickets Structure
#   {
#     "ticket_id": 1,
#     "customer_id": 16,
#     "subject": "Issue 1",
#     "priority": "high",
#     "created_at": "2026-01-30T03:46:48.375896",
#     "status": "closed"
#   },

class Tickets(BaseModel):
    """
    the data model for support_tickets.json
    """
    ticket_id: int
    customer_id: int
    subject: str
    priority: str
    created_at: str
    status: str

class TicketResponse(DataResponse):
    """
    special response model for support tickets so that it is easy for
    us and the LLM to distinguish it from customer and analytics response models
    """
    data: List[Tickets]

class SourcePayloadCRM(SourcePayload):
    """
    the input json payload for get_data_crm()
    """
    filterParameter: Literal["customer_id", "name", "email", "created_at", "status"]
    filterValue: str | int | EmailStr

class SourcePayloadSupport(SourcePayload):
    """
    the input json payload for get_data_support()
    """
    filterParameter: Literal["ticket_id", "customer_id", "subject", "priority", "created_at","status"]

class SourcePayloadAnalytics(SourcePayload):
    """
    the input json payload for get_data_analytics()
    """
    filterParameter: Literal["metric", "date", "value"]