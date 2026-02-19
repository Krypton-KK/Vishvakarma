
from typing import List, Dict
from app.config import settings
from app.models.domain_models import Customer, Tickets, Analytics


def apply_voice_limits(data: List[Customer|Tickets|Analytics],
                       limit:int = settings.MAX_RESULTS) -> List[Customer|Tickets|Analytics]:
    f"""
    Applies voice limits to a list of customer or analytics or ticket data that is fetched 
    from the database. Makes it so that the voice feels more natural and helps keep the 
    content short and sweet
    
    :param data: List[Customer|Tickets|Analytics]. input list to limit.
    :param limit: int. the amount of objects to limit to. {settings.MAX_RESULTS} by default.
    :return: List[Customer|Tickets|Analytics]. truncated values.
    """
    return data[:limit]
