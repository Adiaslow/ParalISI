# src/paralisi/core/interfaces/quality_metric.py
from typing import Protocol
from numpy.typing import NDArray

class QualityMetric(Protocol):
    """Interface for quality assessment metrics."""
    def compute(self, data: NDArray) -> float:
        ...
