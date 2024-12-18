# src/paralisi/core/interfaces/map_analyzer.py
from typing import Protocol, Dict, Any
from numpy.typing import NDArray

class MapAnalyzer(Protocol):
    """Interface for analyzing retinotopic maps."""
    def analyze(self, data: NDArray) -> Dict[str, Any]:
        ...
