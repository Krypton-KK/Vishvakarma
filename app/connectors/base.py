# This tries to mimic how a SQL interface works cause
# I don't have one and since we have JSON stuff we can
# parse it using pydantic and keep it in memory in lists
# for retrival.

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseConnector(ABC):

    @abstractmethod
    def fetch(self, **kwargs) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def query(self, filterParameter: str, filterValue: str | int, returnCount: int = 5, sortAscending: bool = True) -> tuple[list[Any], int]:
        pass