# src/pyisi/core/interfaces.py
"""Core interfaces and protocols for the PyISI package."""

from pathlib import Path
from typing import TypeVar, Protocol, Optional
from numpy.typing import NDArray

from .data_types import RawData, ProcessedData

T = TypeVar('T')

class DataLoader(Protocol):
    """Interface for data loading strategies."""

    def load(self, path: Path) -> RawData:
        """Load data from the given path."""
        ...

    def supports_format(self, path: Path) -> bool:
        """Check if this loader supports the given file format."""
        ...

class DataProcessor(Protocol):
    """Interface for data processing strategies."""

    def process(self, data: RawData) -> ProcessedData:
        """Process raw data into processed form."""
        ...

    def validate(self, data: RawData) -> bool:
        """Validate that the data can be processed."""
        ...

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

class ImageFilter(Protocol):
    """Interface for image filtering operations."""
    def apply(self, data: NDArray) -> NDArray:
        ...

class ImageRegistration(Protocol):
    """Interface for image registration operations."""
    def register(self, reference: NDArray, target: NDArray) -> NDArray:
        ...

class SignalProcessor(Protocol):
    """Interface for signal processing operations."""
    def process(self, data: NDArray) -> NDArray:
        ...

class QualityMetric(Protocol):
    """Interface for quality assessment metrics."""
    def compute(self, data: NDArray) -> float:
        ...

class MapAnalyzer(Protocol):
    """Interface for analyzing retinotopic maps."""
    def analyze(self, data: NDArray) -> Dict[str, Any]:
        ...

class StatisticalTest(Protocol):
    """Interface for statistical analysis."""
    def test(self, data1: NDArray, data2: NDArray) -> Dict[str, Any]:
        ...
