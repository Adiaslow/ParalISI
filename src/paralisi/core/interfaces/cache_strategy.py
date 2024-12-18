# src/paralisi/core/interfaces/cache_strategy.py
from typing import Protocol, TypeVar, Optional

T = TypeVar('T')

class CacheStrategy(Protocol[T]):
    """Interface for caching strategies."""

    def get(self, key: str) -> Optional[T]:
        """Retrieve item from cache."""
        ...

    def put(self, key: str, value: T) -> None:
        """Store item in cache."""
        ...

    def clear(self) -> None:
        """Clear the cache."""
        ...
