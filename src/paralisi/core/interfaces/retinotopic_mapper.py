# src/paralisi/core/interfaces/retinotopic_mapper.py

from typing import Protocol, Tuple, Dict
from numpy.typing import NDArray

class RetinotopicMapper(Protocol):
    """Interface for retinotopic mapping operations."""
    def analyze_retinotopy(self, horizontal_responses: NDArray, vertical_responses: NDArray) -> Dict[str, NDArray]:
        ...
