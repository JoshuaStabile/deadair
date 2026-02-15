from abc import ABC, abstractmethod
from typing import Any, Iterable


class DB(ABC):
    """
    Abstract database interface.
    All concrete DB implementations must inherit this.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the connection."""
        pass

    @abstractmethod
    def execute(self, query: str, params: Iterable[Any] = ()) -> None:
        """Execute a write query (INSERT/UPDATE/DELETE)."""
        pass
