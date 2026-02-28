from abc import ABC, abstractmethod
from typing import Any, Iterable
from enum import Enum

class ConnectionMode(Enum):
    SINGLE = "single"
    THREAD_LOCAL = "thread_local"

class Database(ABC):
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

    @abstractmethod
    def fetch(self, query: str, params: Iterable[Any] = ()) -> None:
        """Execute a fetch query (SELECT)."""
        pass
