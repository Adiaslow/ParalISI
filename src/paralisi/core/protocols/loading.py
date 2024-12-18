# src/paralisi/core/protocols/loading.py
"""Data loading protocols."""

from pathlib import Path
from typing import Protocol
from ..data.data import RawData

class DataLoader(Protocol):
    """Interface for data loading strategies."""

    def load(self, path: Path) -> RawData:
        """Load data from the given path."""
        ...

    def supports_format(self, path: Path) -> bool:
        """Check if this loader supports the given file format."""
        ...
