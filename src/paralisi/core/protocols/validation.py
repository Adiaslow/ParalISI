# src/paralisi/core/protocols/validation.py
"""Data validation protocols."""

from typing import Protocol
from ..data.data import RawData

class DataValidator(Protocol):
    """Interface for data validation strategies."""

    def validate(self, data: RawData) -> bool:
        """Validate raw data."""
        ...

    def get_validation_errors(self) -> list[str]:
        """Get list of validation errors."""
        ...
