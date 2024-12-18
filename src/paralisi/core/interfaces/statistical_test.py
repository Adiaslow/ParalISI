# src/paralisi/core/interfaces/statistical_test.py
from typing import Protocol, Dict, Any
from numpy.typing import NDArray

class StatisticalTest(Protocol):
    """Interface for statistical analysis."""
    def test(self, data1: NDArray, data2: NDArray) -> Dict[str, Any]:
        ...
