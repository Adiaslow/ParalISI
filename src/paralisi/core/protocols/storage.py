# src/paralisi/core/protocols/storage.py
"""Data storage protocols."""

from typing import Protocol
from pathlib import Path
from ..data.data import ProcessedData

class DataStorage(Protocol):
    """Interface for data storage strategies."""

    def save(self, data: ProcessedData, path: Path) -> None:
        """Save processed data to storage."""
        ...

    def exists(self, path: Path) -> bool:
        """Check if data exists at path."""
        ...
