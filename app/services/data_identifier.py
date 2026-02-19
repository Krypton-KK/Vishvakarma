
from typing import List, Dict

from typing_extensions import deprecated

from app.models.domain_models import Customer, Analytics, Tickets


@deprecated("use identify_data instead")
def identify_data_type(data: List[Dict]) -> str:
    if not data:
        return "empty"
    if "date" in data[0]:
        return "time_series"
    if "ticket_id" in data[0]:
        return "tabular_support"
    if "customer_id" in data[0]:
        return "tabular_crm"
    return "unknown"

def identify_data(param: str, vals: List[Customer | Analytics | Tickets]) -> str:
    if not param:
        return "empty"
    if "date" in vals[0].model_dump().keys():
        return "time_series"
    if "ticket_id" in vals[0].model_dump().keys():
        return "tabular_support"
    if "customer_id" in vals[0].model_dump().keys():
        return "tabular_crm"
    return "unknown"