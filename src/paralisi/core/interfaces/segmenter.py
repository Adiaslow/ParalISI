# src/paralisi/core/interfaces/segmenter.py

from typing import Protocol, Tuple, Dict
from numpy.typing import NDArray
from ...core.data.area_data import AreaData

class Segmenter(Protocol):
    """Interface for segmentation operations."""
    def apply(self, data: Tuple[NDArray, NDArray], pixpermm: float) -> Dict[str, AreaData]:
        ...
