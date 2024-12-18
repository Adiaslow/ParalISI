# src/pyisi/core/protocols/processing.py
"""Data processing protocols."""

from typing import Protocol
from ..types.data_types import RawData, ProcessedData

class DataProcessor(Protocol):
    """Interface for data processing strategies."""

    def process(self, data: RawData) -> ProcessedData:
        """Process raw data into processed form."""
        ...

    def validate(self, data: RawData) -> bool:
        """Validate that the data can be processed."""
        ...
