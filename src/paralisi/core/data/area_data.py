# src/paralisi/core/data/area_data.py

"""Data class for visual area information."""

from dataclasses import dataclass
from typing import List, Tuple
from numpy.typing import NDArray

@dataclass
class AreaData:
    """Information about a detected visual area."""
    id: int
    name: str
    boundary: NDArray  # Boolean mask of area boundary
    center: Tuple[float, float]  # Center of mass coordinates
    sign: float  # Visual field sign (1 or -1)
    size: float  # Area size in mm²
    neighbors: List[int]  # IDs of neighboring areas
