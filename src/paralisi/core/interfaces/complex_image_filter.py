# src/paralisi/core/interfaces/complex_image_filter.py

from typing import Protocol, Tuple, Dict
from numpy.typing import NDArray
from ...core.data.area_data import AreaData

class ComplexImageFilter(Protocol):
    """Interface for complex image filtering operations."""
    def apply(self, data: Tuple[NDArray, NDArray], pixpermm: float) -> Dict[str, AreaData]:
        ...
